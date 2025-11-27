import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from enum import Enum
from python.helpers import files
from agent import Agent

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class PlanTask:
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    subtasks: List["PlanTask"] = field(default_factory=list)
    result: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "subtasks": [t.to_dict() for t in self.subtasks],
            "result": self.result
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlanTask":
        task = cls(
            id=data["id"],
            description=data["description"],
            status=TaskStatus(data.get("status", "pending")),
            result=data.get("result")
        )
        task.subtasks = [cls.from_dict(t) for t in data.get("subtasks", [])]
        return task

@dataclass
class Plan:
    goal: str
    tasks: List[PlanTask]
    success_criteria: List[str] = field(default_factory=list)
    avoid_list: List[str] = field(default_factory=list)
    status: str = "active" # active, completed, failed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "tasks": [t.to_dict() for t in self.tasks],
            "success_criteria": self.success_criteria,
            "avoid_list": self.avoid_list,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Plan":
        return cls(
            goal=data["goal"],
            tasks=[PlanTask.from_dict(t) for t in data.get("tasks", [])],
            success_criteria=data.get("success_criteria", []),
            avoid_list=data.get("avoid_list", []),
            status=data.get("status", "active")
        )

class Planner:
    _instances: Dict[str, "Planner"] = {}

    def __init__(self, agent: Agent):
        self.agent = agent
        self.plan: Optional[Plan] = None
        self._load()

    @classmethod
    def get(cls, agent: Agent) -> "Planner":
        if agent.context.id not in cls._instances:
            cls._instances[agent.context.id] = cls(agent)
        return cls._instances[agent.context.id]

    def _get_file_path(self) -> str:
        # Save in tmp/planner/{context_id}.json
        folder = files.get_abs_path("tmp", "planner")
        if not os.path.exists(folder):
            os.makedirs(folder)
        return os.path.join(folder, f"{self.agent.context.id}.json")

    def _load(self):
        path = self._get_file_path()
        if os.path.exists(path):
            try:
                data = json.loads(files.read_file(path))
                self.plan = Plan.from_dict(data)
            except Exception as e:
                print(f"Error loading plan: {e}")
                self.plan = None

    def save(self):
        if self.plan:
            path = self._get_file_path()
            files.write_file(path, json.dumps(self.plan.to_dict(), indent=2))
        else:
            # If plan is cleared, delete the file
            path = self._get_file_path()
            if os.path.exists(path):
                os.remove(path)

    def create_plan(self, goal: str, tasks: List[Dict[str, Any]], success_criteria: List[str] = [], avoid_list: List[str] = []):
        plan_tasks = self._parse_tasks(tasks)

        self.plan = Plan(
            goal=goal,
            tasks=plan_tasks,
            success_criteria=success_criteria,
            avoid_list=avoid_list
        )
        self.save()

    def _parse_tasks(self, tasks_data: List[Dict[str, Any]], parent_id: str = "") -> List[PlanTask]:
        plan_tasks = []
        for i, t in enumerate(tasks_data):
            # Assign ID if not provided, 1-based index, use dot notation for subtasks
            # If ID is provided in data, use it. Otherwise generate one.
            tid = t.get("id")
            if not tid:
                tid = f"{parent_id}.{i + 1}" if parent_id else str(i + 1)

            task = PlanTask(
                id=tid,
                description=t["description"],
                status=TaskStatus.PENDING
            )

            subtasks_data = t.get("subtasks", [])
            if subtasks_data:
                task.subtasks = self._parse_tasks(subtasks_data, tid)

            plan_tasks.append(task)
        return plan_tasks

    def update_task(self, task_id: str, status: Optional[str] = None, result: Optional[str] = None):
        if not self.plan:
            return False

        task = self._find_task(task_id, self.plan.tasks)
        if task:
            if status:
                task.status = TaskStatus(status)
            if result:
                task.result = result
            self.save()
            return True
        return False

    def _find_task(self, task_id: str, tasks: List[PlanTask]) -> Optional[PlanTask]:
        for task in tasks:
            if task.id == task_id:
                return task
            found = self._find_task(task_id, task.subtasks)
            if found:
                return found
        return None

    def get_status_report(self) -> str:
        if not self.plan:
            return "No active plan."

        report = f"# Plan: {self.plan.goal}\n"
        report += f"Status: {self.plan.status}\n\n"

        if self.plan.success_criteria:
            report += "## Success Criteria:\n"
            for c in self.plan.success_criteria:
                report += f"- {c}\n"
            report += "\n"

        if self.plan.avoid_list:
            report += "## Avoid:\n"
            for a in self.plan.avoid_list:
                report += f"- {a}\n"
            report += "\n"

        report += "## Tasks:\n"
        for task in self.plan.tasks:
            report += self._format_task(task, 0)

        return report

    def _format_task(self, task: PlanTask, level: int) -> str:
        indent = "  " * level
        icon = {
            TaskStatus.PENDING: "☐",
            TaskStatus.IN_PROGRESS: "▶",
            TaskStatus.DONE: "☑",
            TaskStatus.FAILED: "☒",
            TaskStatus.SKIPPED: "⊖"
        }.get(task.status, "☐")

        line = f"{indent}{icon} **{task.id}**: {task.description}"
        if task.result:
             line += f"\n{indent}  Result: {task.result}"
        line += "\n"

        for sub in task.subtasks:
            line += self._format_task(sub, level + 1)

        return line
