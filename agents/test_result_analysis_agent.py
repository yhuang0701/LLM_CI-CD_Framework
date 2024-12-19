# test_result_analysis_agent.py
from metagpt.roles import Role
from metagpt.actions import Action
from metagpt.logs import logger
from metagpt.team import Message
from agents.actions import AnalyzeBuildTestResults, GenerateAndRunTests  # Import GenerateAndRunTests

class TestResultAnalysisAgent(Role):
    name: str = "Test Result Analysis Agent"
    profile: str = "Handles analysis of results from testing pull requests"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([AnalyzeBuildTestResults]) # Configures the agent to execute the AnalyzeBuildTestResults action.
        self._watch([GenerateAndRunTests]) # Sets up the agent to monitor for GenerateAndRunTests actions, ensuring it responds to test execution outputs.

    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})") # Logging: Records the current action and task.
        todo = self.rc.todo

        # Retrieve test results from memory, searches for the latest GenerateAndRunTests in memory to obtain test results.
        memories = self.get_memories()
        test_results_msg = None
        for m in reversed(memories):
            if m.cause_by == "agents.actions.GenerateAndRunTests":
                test_results_msg = m
                break

        if test_results_msg is None: # If test results are missing, logs a warning and exits, awaiting test execution.
            logger.warning("No test results found in memory. Waiting for TestAgent to complete.")
            return  # Exit the action and wait for the next round

        build_test_output = test_results_msg.content # If test results are present, proceeds to analyze them.

        result = await todo.run(build_test_output)  # Analyze the actual test results

        logger.info("TestResultAnalysisAgent: Test result analysis action completed.")
        logger.info(f"TestResultAnalysisAgent: Analysis result: {result}")

        msg = Message(content=result, role=self.profile, cause_by=type(todo)) # Stores the analysis results in memory for further actions or reporting.
        self.rc.memory.add(msg)
        return msg
