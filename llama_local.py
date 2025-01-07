import os

from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
import logging

query_engine = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_query_engine(name):
    logger.info("initialize_query_engine() name=%s", name)
    # 配置LLM（大语言模型）。模型名为qwen2.5:0.5b
    Settings.llm = Ollama(model="qwen2.5:0.5b", request_timeout=100.0)
    # 配置用于文本嵌入的模型。模型名为quentinz/bge-base-zh-v1.5
    Settings.embed_model = OllamaEmbedding(model_name="quentinz/bge-base-zh-v1.5")
    storage_dir = "./storage/"+name
    logger.info("storage_dir=%s", storage_dir)
    if not os.path.exists(storage_dir):
        documents = SimpleDirectoryReader("./data/"+name).load_data()
        logger.info("documents=%s", documents)
        index = VectorStoreIndex.from_documents(documents, transformations=[SentenceSplitter(chunk_size=256)])
        logger.info("index11=%s", index)
        index.storage_context.persist(persist_dir=storage_dir)
        logger.info("index12=%s", index)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=storage_dir)
        index = load_index_from_storage(storage_context)
        logger.info("index2=%s", index)
    global query_engine
    query_engine[name] = index.as_query_engine(response_mode="tree_summarize")
    logger.info("initialize_query_engine() done!")
