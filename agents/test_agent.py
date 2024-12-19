# test_agent.py
from metagpt.roles import Role
from metagpt.actions import Action
from metagpt.logs import logger
from metagpt.team import Message
from agents.actions import TestPlan, GenerateAndRunTests

class TestAgent(Role):
    name: str = "Test Agent"
    profile: str = "agent handling testing pull requests"
    goal: str = """utilize the test plan and run the pytest""" # Clearly defines the agent's objective to utilize test plans and execute tests using pytest

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([GenerateAndRunTests]) # Configures the agent to execute the GenerateAndRunTests action.
        self._watch([TestPlan]) # Sets up the agent to monitor for TestPlan actions, ensuring it responds to test planning outputs.

    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        # Retrieve the test plan from memory
        memories = self.get_memories()
        test_plan_msg = None
        for m in reversed(memories):
            if m.cause_by == "agents.actions.TestPlan":
                test_plan_msg = m
                break

        if test_plan_msg is None:
            logger.warning("No test plan found in memory. Waiting for TestPlan to be generated.")
            return  # Exit the action and wait for the next round

        test_plan = test_plan_msg.content  # Extract the test plan

        # Retrieve the actual code from memory
        code_msg = None
        for m in reversed(memories):
            if m.cause_by == "metagpt.actions.add_requirement.UserRequirement":
                code_msg = m
                break

        if code_msg is None:
            logger.warning("No code found in memory. Waiting for code to be provided.")
            return  # Exit the action and wait for the next round

        code = code_msg.content  # Extract the code

        result = await todo.run(test_plan, code)

        logger.info("TestAgent: Test action completed.")
        logger.info(f"TestAgent: Result of test: {result}")

        msg = Message(content=result, role=self.profile, cause_by="agents.actions.GenerateAndRunTests")
        self.rc.memory.add(msg)
        return msg