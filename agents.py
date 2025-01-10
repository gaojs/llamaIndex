# https://github.com/datawhalechina/handy-ollama/
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama


def multiply(a: float, b: float) -> float:
    return a * b


# Create FunctionTool instances
multiply_tool = FunctionTool.from_defaults(
    fn=multiply,
    name="MultiplyTool",
    description="A tool that multiplies two floats.",
    return_direct=True
)

# Initialize LLM
llm = Ollama(model="qwen2:0.5b", request_timeout=360.0)

# Initialize ReAct agent with tools
agent = ReActAgent.from_tools([multiply_tool], llm=llm, verbose=True)

res = llm.complete("What is 2.3 × 4.8 ? Calculate step by step")
print(res)

# use agent
response = agent.chat("What is 2.3 × 4.8 ? Calculate step by step")
print(response.response)
