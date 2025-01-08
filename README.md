本示例程序，展示了用ollama本地启动qwen大语言模型。
后端用了flask开源框架，前端用了gradio开源库。

server.py，是服务端程序。可以用命令（python server.py）启动它。
client.py，是客户端程序。可以用命令（python client.py）启动它。
llama_local.py，本地启动LLM大语言模型。
storage目录存放LLM解析后的数据文件。
data目录存放用户上传的原始文件。

启动ollama服务：ollama serve
下载嵌入模型：ollama pull quentinz/bge-base-zh-v1.5
启动qwen模型：ollama run qwen2.5:0.5b
