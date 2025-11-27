from python.helpers.extension import Extension
from python.helpers.planner import Planner

class PlannerLoopPrompt(Extension):
    async def execute(self, **kwargs):
        planner = Planner.get(self.agent)
        if planner.plan and planner.plan.status == "active":
            loop_data = kwargs.get("loop_data")
            if loop_data:
                # Add current plan status to persistent extras so it appears in the context
                loop_data.extras_persistent["current_plan"] = planner.get_status_report()
