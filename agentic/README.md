# Agentic Alignment Testing System

This system uses CrewAI agents to test AI models for alignment faking and other concerning behaviors via the Ollama API.

## Setup

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

This will install:
- `crewai` - Framework for creating AI agent crews
- `crewai-tools` - Pre-built tools for CrewAI agents  
- `requests` - HTTP library for calling Ollama API

### 2. Start Ollama

Make sure Ollama is running on `http://localhost:11434`:

```bash
ollama serve
```

### 3. Pull Required Model

```bash
ollama pull llama3.1:8b
```

## Usage

### Run the Agentic Crew

```bash
cd /Users/vbector/Developer/Research/Insight-Lab-Thesis/agentic
python3 main.py
```

This will:
1. **Red-Teamer Agent**: Tests the model with adversarial prompts using the OllamaTestTool
2. **Evaluator Agent**: Analyzes responses for alignment issues
3. **Investigator Agent**: Provides final audit verdict

### Test the Ollama Tool Standalone

To verify the OllamaTestTool works without running the full crew:

```bash
python3 test_ollama_tool.py
```

## Components

- **`ollama_tool.py`**: Custom CrewAI tool that wraps Ollama API for model testing
- **`agents.py`**: Defines the three agents (red_teamer, evaluator, investigator)
- **`tasks.py`**: Defines tasks for each agent with instructions to use OllamaTestTool
- **`llm_config.py`**: Configures the LLM (Ollama) that powers the agents themselves
- **`main.py`**: Entry point that orchestrates the crew

## How It Works

The key enhancement is the **OllamaTestTool** which allows agents to:
- Make HTTP requests to Ollama API
- Test models with different system and user prompts
- Receive actual model responses for analysis

This bridges the gap between the CrewAI agent framework and the direct Ollama API testing done in the `poc` folder scripts.

## Customization

Edit `main.py` to change:
- `system_prompt`: The model's behavior instructions
- `user_prompt`: The input to test the model with

You can also modify `tasks.py` to test different models or add more test variations.
