import subprocess
import re

from metagpt.actions import Action
from metagpt.logs import logger

def parse_code(rsp, lang="python"):
    pattern = r"```" + lang + r"(.*)```"
    match = re.search(pattern, rsp, re.DOTALL)
    code_text = match.group(1) if match else rsp
    return code_text
    
class TestPlan(Action):
    name: str = "TestPlan"

    PROMPT_TEMPLATE: str = """
    Based on the product requirement, come up with a plan to test the following code. Include what kind of tests you would run and the functions/methods that you would test.
    The code is: {context}
    """

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)

        rsp = await self._aask(prompt)

        return rsp

    
class CodeReviewAgent(Action):
    name: str = "CodeReviewAgent"

    PROMPT_TEMPLATE: str = """
    Context: {context}
    Based on the product requirement, review the code. Include checks for code style, functionality, performance, and security.
    """

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)

        rsp = await self._aask(prompt)

        return rsp

class CodeDocumentAgent(Action):
    name: str = "CodeDocumentAgent"

    PROMPT_TEMPLATE: str = """
    Context: {context}
    Based on the product requirement, document the provided code. 
    Provide documentation for classes, methods, or functions. 
    """

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)

        rsp = await self._aask(prompt)

        return rsp

class RiskAnalysisAgent(Action):
    name: str = "RiskAnalysisAgent"

    PROMPT_TEMPLATE: str = """
     {context} This is the updated content for this release. Please help me evaluate potential system issues based on the following code, such as identifying which functions might be affected and analyzing potential problem points. 
    """

    async def run(self, context: str):
        print("Analysising Risk Report...")
        print('context:', context)

        prompt = self.PROMPT_TEMPLATE.format(context=context)
        print('risk analysis prompt', prompt)
        rsp = await self._aask(prompt)
        print("risk analysis rsp", rsp)
        return rsp

class RiskReportAgent(Action):
    name: str = "RiskReportAgent"

    PROMPT_TEMPLATE: str = """
    {context} Based on the information above, please summarize the risk information for this update. Format it using Markdown syntax, and include the image ./function_risk_graph.png at the end of the document. Please only export markdown content without other things.
    """

    async def run(self, context: str):
        print("Run Risk Report...")
        print('context:', context)
        prompt = self.PROMPT_TEMPLATE.format(context=context)

        rsp = await self._aask(prompt)

        filename = "update_report.md"

        try:
            print("try storing")
            with open(filename, "w") as file:
                file.write(rsp.split("```")[1])
            print(f"Content successfully written to {filename}")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

        return rsp

class GenerateAndRunTests(Action):
    name: str = "GenerateAndRunTests"

    async def run(self):
        result = subprocess.run(["python", "-c", "print('Test code command placeholder')"], capture_output=True, text=True).stdout
        logger.info(f"{result=}")
        return result

    
class AnalyzeBuildTestResults(Action):
    name: str = "AnalyzeBuildTestResults"

    PROMPT_TEMPLATE: str = """
    Analyzing build and test results: {output}
    """

    async def run(self, build_test_output: str):
        prompt = self.PROMPT_TEMPLATE.format(output=build_test_output)

        rsp = await self._aask(prompt)

        return rsp