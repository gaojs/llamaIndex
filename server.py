from flask import Flask
from flask import request
import llama_local
app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/query", methods=["GET"])
def query_index():
    engine_name = request.args.get("name", None)
    if engine_name not in llama_local.query_engine:
        llama_local.initialize_query_engine(engine_name)

    query_text = request.args.get("text", None)
    if query_text is None:
        return (
            "No text found, please include a ?text=blah parameter in the URL",
            400,
        )
    response = llama_local.query_engine[engine_name].query(query_text)
    return str(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5601)
