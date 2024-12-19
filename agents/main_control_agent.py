from metagpt.roles import Role
from metagpt.actions import  UserRequirement
from metagpt.team import Message

from agents.actions import TestPlan, CodeDocumentAgent, CodeReviewAgent, RiskAnalysisAgent, RiskReportAgent


class MainControlAgent(Role):
    name: str = "Main Control Agent"
    profile: str = "Coordinator of the CI/CD pipeline"
    goal: str = """To coordinate a multi-agent LLM-driven automatic CI/CD pipeline. Take steps to execuate the code review tasks one by one"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([TestPlan, CodeReviewAgent, CodeDocumentAgent, RiskAnalysisAgent, RiskReportAgent])
        self._set_react_mode(react_mode="by_order")
        self._watch([UserRequirement])

    async def _act(self):
        todo = self.rc.todo
        context = self.get_memories()
        result = await todo.run(context=context)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
