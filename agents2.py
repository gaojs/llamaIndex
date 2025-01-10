# https://docs.llamaindex.ai/en/stable/examples/agent/react_agent/
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama


def multiply(a: int, b: int) -> int:
    return a * b


def add(a: int, b: int) -> int:
    return a + b


multiply_tool = FunctionTool.from_defaults(
    fn=multiply,
    name="MultiplyTool",
    description="A tool that multiplies two int.",
    return_direct=True
)
add_tool = FunctionTool.from_defaults(
    fn=add,
    name="AddTool",
    description="A tool that add two int.",
    return_direct=True
)

# Initialize LLM
llm = Ollama(model="qwen2.5:0.5b", request_timeout=360.0)
agent = ReActAgent.from_tools([multiply_tool, add_tool], llm=llm, verbose=True)

res = llm.complete("What is 2+2*4")
print(res)

agent.chat("What is 2+2*4")
