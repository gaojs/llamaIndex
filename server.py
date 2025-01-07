from flask import Flask
from flask import request
from flask import jsonify
import llama_local
import logging
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def home():
    return "Hello World!"


@app.route("/query", methods=["GET"])
def query():
    try:
        engine_name = request.args.get("name", None)
        logger.info("engine_name=%s", engine_name)
        if not engine_name:
            return jsonify({"error": "Engine name is required!"}), 400
        if engine_name not in llama_local.query_engine:
            llama_local.initialize_query_engine(engine_name)

        query_text = request.args.get("text", None)
        logger.info("query_text=%s", query_text)
        if not query_text:
            return jsonify({"error": "Query text is required!"}), 400
        response = llama_local.query_engine[engine_name].query(query_text)
        logger.info("response=%s", str(response))
        return jsonify({"response": response}), 200
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred!"}), 500


if __name__ == "__main__":
    # 在指定 IP 和端口上运行 Flask 应用。
    app.run(host="0.0.0.0", port=8099)
