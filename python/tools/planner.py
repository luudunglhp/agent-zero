from python.helpers.tool import Tool, Response
from python.helpers.planner import Planner
from python.helpers.planner import TaskStatus
import json

class PlannerTool(Tool):
    async def execute(self, **kwargs):
        planner = Planner.get(self.agent)

        if self.method == "create_plan":
            return await self.create_plan(planner, **kwargs)
        elif self.method == "update_task":
            return await self.update_task(planner, **kwargs)
        elif self.method == "get_plan":
            return await self.get_plan(planner, **kwargs)
        elif self.method == "mark_plan_completed":
            return await self.mark_plan_completed(planner, **kwargs)
        else:
            return Response(message=f"Unknown method '{self.method}'", break_loop=False)

    async def create_plan(self, planner: Planner, **kwargs):
        goal = kwargs.get("goal")
        tasks = kwargs.get("tasks", [])
        success_criteria = kwargs.get("success_criteria", [])
        avoid_list = kwargs.get("avoid_list", [])

        if not goal:
            return Response(message="Goal is required", break_loop=False)

        if not tasks:
             return Response(message="At least one task is required", break_loop=False)

        planner.create_plan(goal, tasks, success_criteria, avoid_list)
        return Response(message="Plan created successfully.\n" + planner.get_status_report(), break_loop=False)

    async def update_task(self, planner: Planner, **kwargs):
        task_id = kwargs.get("task_id")
        status = kwargs.get("status")
        result = kwargs.get("result")

        if not task_id:
            return Response(message="Task ID is required", break_loop=False)

        # Normalize status to lowercase if provided
        if status:
            try:
                # Validate status against Enum, but allow case-insensitive input
                status_enum = TaskStatus(status.lower())
                status = status_enum.value
            except ValueError:
                valid_statuses = [e.value for e in TaskStatus]
                return Response(message=f"Invalid status '{status}'. Valid statuses are: {', '.join(valid_statuses)}", break_loop=False)

        if planner.update_task(str(task_id), status, result):
            return Response(message=f"Task {task_id} updated.\n" + planner.get_status_report(), break_loop=False)
        else:
            return Response(message=f"Task {task_id} not found or no active plan.", break_loop=False)

    async def get_plan(self, planner: Planner, **kwargs):
        return Response(message=planner.get_status_report(), break_loop=False)

    async def mark_plan_completed(self, planner: Planner, **kwargs):
        if planner.plan:
            planner.plan.status = "completed"
            planner.save()
            return Response(message="Plan marked as completed.", break_loop=False)
        return Response(message="No active plan.", break_loop=False)
