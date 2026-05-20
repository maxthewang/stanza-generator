let currentPoem = "";

async function loadStanza() {
    const response = await fetch("/stanza");
    const data = await response.json();

    currentPoem = data.rows.map(row => row.line).join("\n");

    const poem = document.getElementById("poem");

    poem.innerHTML = data.rows.map(row => `
        <div>${row.line}</div>
        <div style="color: gray;">${row.gid}</div>
    `).join("");
}

async function copyPoem() {
    await navigator.clipboard.writeText(currentPoem);
}

loadStanza();