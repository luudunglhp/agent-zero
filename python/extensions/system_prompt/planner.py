from python.helpers.extension import Extension
from python.helpers.planner import Planner

class PlannerSystemPrompt(Extension):
    async def execute(self, **kwargs):
        system_prompt = kwargs.get("system_prompt")
        if system_prompt is None:
            return

        instruction = """
# Planner
You have access to a Planner tool.
- Use `planner:create_plan` to break down complex goals into tasks.
  - Arguments:
    - `goal`: string, the main goal.
    - `tasks`: list of dictionaries, each containing `description` (string) and optional `id` (string) or `subtasks` (list of same structure).
    - `success_criteria`: list of strings.
    - `avoid_list`: list of strings.
- Use `planner:update_task` to mark tasks as `in_progress`, `done`, or `failed`, and record results.
- Check the plan status regularly.
- Keep the plan up to date.
- When all tasks are done and the goal is achieved, use `planner:mark_plan_completed`.
"""
        system_prompt.append(instruction)
