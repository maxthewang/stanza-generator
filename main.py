import os

import duckdb
from datasets import load_dataset
from flask import Flask, jsonify, render_template

app = Flask(__name__)

dataset = load_dataset("biglam/gutenberg-poetry-corpus", split="train")

duckdb.register("train", dataset.data.table)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stanza")
def stanza():
    results = duckdb.sql("""
        SELECT *
        FROM train
        ORDER BY random()
        LIMIT 4
    """).fetchall()

    return jsonify(
        {"rows": [{"line": row[0], "gid": row[1]} for row in results]}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
