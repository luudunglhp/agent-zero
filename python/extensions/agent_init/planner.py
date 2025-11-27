from python.helpers.extension import Extension
from python.helpers.planner import Planner

class PlannerInit(Extension):
    async def execute(self, **kwargs):
        # Initialize planner for this agent context
        Planner.get(self.agent)
