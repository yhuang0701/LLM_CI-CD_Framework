import asyncio

from metagpt.team import Team

from agents.main_control_agent import MainControlAgent
from agents.test_agent import TestAgent
from agents.test_result_analysis_agent import TestResultAnalysisAgent

async def main(initial_prompt):
    cicd_team = Team()
    cicd_team.hire([
        MainControlAgent(),
        TestAgent(),
        TestResultAnalysisAgent(),
        # other agents implemented as an 'Action of the MainControlAgent', following the MetaGPT structure
    ])

    cicd_team.invest(investment=0.5)
    cicd_team.run_project(initial_prompt)

    await cicd_team.run(n_round=10)

if __name__ == "__main__":

    project = 'source_project/example_project.py'
    diff = 'diff.txt'

    with open(project, 'r') as file:
        project = file.read()
    
    with open(diff, 'r') as file:
        diff_txt = file.read()
    
    initial_prompt = f'Last Git Commit Diff:\n{diff_txt}\n=====\nProject Code:\n{project}'

    print(f'Staring CICD Code Review Process with initial prompt:{initial_prompt}')
    asyncio.run(main(initial_prompt))