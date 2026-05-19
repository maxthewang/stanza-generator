from datasets import load_dataset
from flask import Flask, jsonify
import duckdb
import os

app = Flask(__name__)

dataset = load_dataset(
    "biglam/gutenberg-poetry-corpus",
    split="train"
)

duckdb.register("train", dataset.data.table)

HTML = """
<!doctype html>
<html>
<body style="padding: 40px;">

<div id="poem"
     style="display: grid; grid-template-columns: auto 2fr; gap: 8px 24px; font-size: 2rem;">
</div>

<button onclick="loadStanza()"
        style="font-size: 2rem; margin-top: 30px;">
    New Stanza
</button>

<script>
async function loadStanza() {
    const response = await fetch("/stanza");
    const data = await response.json();

    const poem = document.getElementById("poem");

    poem.innerHTML = data.rows.map(row => `
        <div>${row.line}</div>
        <div style="color: gray;">${row.gid}</div>
    `).join("");
}

loadStanza();
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return HTML

@app.route("/stanza")
def stanza():
    results = duckdb.sql("""
        SELECT *
        FROM train
        ORDER BY random()
        LIMIT 4
    """).fetchall()

    return jsonify({
        "rows": [
            {
                "line": row[0],
                "gid": row[1]
            }
            for row in results
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))