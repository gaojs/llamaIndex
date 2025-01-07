import os

from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

# 增加日志信息
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

query_engine = {}

def initialize_query_engine(name):
    Settings.llm = Ollama(model="qwen2.5:7b", request_timeout=100.0)
    Settings.embed_model = OllamaEmbedding(model_name = "quentinz/bge-base-zh-v1.5")

    storge_dir = "./storage/"+name
    if not os.path.exists(storge_dir):
        documents = SimpleDirectoryReader("./data/"+name).load_data()
        index = VectorStoreIndex.from_documents(documents, transformations=[SentenceSplitter(chunk_size=256)])
        index.storage_context.persist(persist_dir=storge_dir)

    else:
        storage_context = StorageContext.from_defaults(persist_dir=storge_dir)
        index = load_index_from_storage(storage_context)

    global query_engine
    query_engine[name] = index.as_query_engine(response_mode="tree_summarize")
