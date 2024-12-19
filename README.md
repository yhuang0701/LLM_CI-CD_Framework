# A Multi-agent LLM-Driven CI/CD System with Code Review Enhancement
## Install

```bash
conda create -n cicd_project python=3.11
conda activate cicd_project
pip install -r requirements.txt
```

Copy the following code to `~/.metagpt/config2.yaml`. Create this file if it does not exist.
```yaml
llm:
  api_type: "openai"  # or azure / ollama / open_llm etc. Check LLMType for more options
  model: "gpt-4-1106-prevoew"  # or gpt-3.5-turbo-1106, or other latest versions
  base_url: "https://api.openai.com/v1"  # or forward url / other llm url
  api_key: ""
```

Replace `api_key` with the OpenAI API key.

## Run

### Run Locally

(OPTIONALLY) First store the last commit diff in diff.txt by

```bash
git diff HEAD~1 HEAD > diff.txt
```

This will allow the system to access the last patch diff for agent to analyze (e.g. the Risk Analysis Agent)

(this process is also automatically completed in the GitHub Action version)

Start the main process:

```bash
python main.py
```

this run will use the example source project by defaul: `example_project.py`

