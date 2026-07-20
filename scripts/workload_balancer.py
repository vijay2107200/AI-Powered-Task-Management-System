"""
workload_balancer.py
=====================
Heuristic assignee-recommendation engine for the AI-Powered Task Management
System (Week 3 - Workload Balancing).

Why a heuristic and not an ML model
------------------------------------
The dataset records *which* assignee got each task, but not whether that
assignment was actually a good one (no completion-quality signal, no
rework/reassignment flags, no SLA-breach outcome, no assignee satisfaction
signal). Without a labeled outcome to predict, there is nothing for a
supervised model to learn from - training a classifier/regressor on
"who historically got this task" would just learn to reproduce whatever
assignment process (random / round-robin / manual) generated the existing
`assignee_id` column, not to make *good* assignments.

A transparent, hand-specified heuristic scoring function is the right tool
here: it lets us directly encode the staffing rules we actually want
(don't overload people, match seniority to task difficulty, prefer idle
staff) and is fully auditable and tunable, which matters for a system that
affects real people's workloads. If/when the project collects real outcome
labels (e.g. did the task get done on time, was it reassigned), an ML
ranking model could be trained to *replace or refine* this heuristic's
weights.

Scoring approach
-----------------
For a candidate assignee `a` and task `t`:

    score(a, t) = experience_fit(a, t) - workload_penalty(a)

- ``experience_fit``: a task's priority and estimated effort combine into a
  "required experience" level. Under-qualified assignees are penalized
  proportionally to the shortfall; over-qualified assignees get a small,
  *capped* bonus (so the single most senior person doesn't get every task -
  we don't want to burn out your best people on trivial work).
- ``workload_penalty``: proportional to the assignee's current open task
  count, so busier people are less likely to get the next task.
- Ties (equal score) are broken by fewest current open tasks, then by
  `assignee_id` for determinism.

The assignee with the **highest** score is recommended.
"""

from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


PRIORITY_WEIGHT = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}

# Tunable heuristic weights - documented here so they're easy to find and
# adjust without hunting through the scoring logic itself.
WEIGHTS = {
    "underqualified_penalty": 3.0,   # per year of experience shortfall
    "overqualified_bonus": 0.5,      # per year of surplus experience
    "overqualified_bonus_cap": 3.0,  # cap the surplus bonus (years)
    "workload_penalty": 1.2,         # per current open task
    "effort_experience_scale": 6.0,  # hours-per-experience-year divisor
    # calibrated against the dataset: (priority_weight * estimated_hours)
    # has median 11.0 and p90 32.4 across all tasks; dividing by 6 maps the
    # median task to ~1.8 "required years" and the 90th percentile to ~5.4,
    # comfortably inside the real assignee experience range (0.8-14.6 yrs)
    # so only genuinely demanding tasks (high priority + high effort) push
    # toward requiring the most senior staff.
}


@dataclass
class Assignee:
    assignee_id: str
    experience_years: float
    open_tasks: int


@dataclass
class ScoredCandidate:
    assignee_id: str
    score: float
    required_experience: float
    experience_component: float
    workload_component: float


class WorkloadBalancer:
    """Stateful heuristic assignee recommender.

    Tracks each assignee's current open-task count internally and updates
    it every time `assign()` is called, so repeated calls reflect a
    live/simulated workload rather than a static snapshot.
    """

    def __init__(self, users: dict[str, Assignee], weights: dict = None):
        self.users = users
        self.weights = weights or WEIGHTS

    @classmethod
    def from_dataframe(cls, users_df: pd.DataFrame) -> "WorkloadBalancer":
        """Build a balancer from a DataFrame with one row per assignee and
        columns: assignee_id, experience_years, open_tasks."""
        users = {
            row.assignee_id: Assignee(
                assignee_id=row.assignee_id,
                experience_years=float(row.experience_years),
                open_tasks=int(row.open_tasks),
            )
            for row in users_df.itertuples()
        }
        return cls(users)

    def required_experience(self, priority: str, estimated_hours: float) -> float:
        w = PRIORITY_WEIGHT.get(priority, 2)
        return (w * estimated_hours) / self.weights["effort_experience_scale"]

    def _score(self, a: Assignee, priority: str, estimated_hours: float) -> ScoredCandidate:
        required = self.required_experience(priority, estimated_hours)
        gap = a.experience_years - required

        if gap < 0:
            exp_component = gap * self.weights["underqualified_penalty"]  # negative
        else:
            capped_surplus = min(gap, self.weights["overqualified_bonus_cap"])
            exp_component = capped_surplus * self.weights["overqualified_bonus"]

        workload_component = -a.open_tasks * self.weights["workload_penalty"]

        return ScoredCandidate(
            assignee_id=a.assignee_id,
            score=exp_component + workload_component,
            required_experience=required,
            experience_component=exp_component,
            workload_component=workload_component,
        )

    def rank_candidates(self, priority: str, estimated_hours: float) -> list[ScoredCandidate]:
        scored = [
            self._score(a, priority, estimated_hours) for a in self.users.values()
        ]
        scored.sort(
            key=lambda c: (
                -c.score,
                self.users[c.assignee_id].open_tasks,
                c.assignee_id,
            )
        )
        return scored

    def suggest_assignee(self, priority: str, estimated_hours: float) -> ScoredCandidate:
        """Return the top-ranked candidate without mutating state."""
        return self.rank_candidates(priority, estimated_hours)[0]

    def assign(self, priority: str, estimated_hours: float) -> ScoredCandidate:
        """Suggest the best assignee AND record the assignment (increments
        that assignee's simulated open_tasks count by 1)."""
        best = self.suggest_assignee(priority, estimated_hours)
        self.users[best.assignee_id].open_tasks += 1
        return best

    def workload_snapshot(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "assignee_id": a.assignee_id,
                    "experience_years": a.experience_years,
                    "open_tasks": a.open_tasks,
                }
                for a in self.users.values()
            ]
        ).sort_values("assignee_id").reset_index(drop=True)
