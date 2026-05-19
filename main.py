from datasets import load_dataset
from flask import Flask
import duckdb
import os

app = Flask(__name__)

dataset = load_dataset(
    "biglam/gutenberg-poetry-corpus",
    split="train"
)

table = dataset.data.table
duckdb.register("train", table)

HTML = """
<!doctype html>
<html>
<body style="padding: 40px;">

<div style="display: grid; grid-template-columns: auto 2fr; gap: 8px 24px; font-size: 2rem;">
    {{ rows }}
</div>

<form method="get" style="margin-top: 30px;">
    <button type="submit" style="font-size: 2rem;">
        New Quatrain
    </button>
</form>

</body>
</html>
"""

@app.route("/")
def index():
    results = duckdb.sql("""
        SELECT *
        FROM train
        ORDER BY random()
        LIMIT 4
    """).fetchall()

    rows_html = ""

    for row in results:
        line = row[0]
        gid = row[1]

        rows_html += f"""
        <div>{line}</div>
        <div style="color: gray;">{gid}</div>
        """

    return HTML.replace("{{ rows }}", rows_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))