let stanzaData = {};

async function loadStanza() {
	const status = document.getElementById("status");

	status.textContent = "Loading...";

	try {
		const response = await fetch("/stanza");

		if (!response.ok) {
			throw new Error("Server error");
		}

		const data = await response.json();
		stanzaData = data;

		const poem = document.getElementById("poem");
		poem.innerHTML = data.rows
			.map(
				(row) => `
            <div>${row.line}</div>
            <div style="color: gray;">${row.gid}</div>
        `,
			)
			.join("");

		status.textContent = "";
	} catch (error) {
		status.textContent = "Query failed. Refresh the page.";
	}
}

async function copyPoem() {
	await navigator.clipboard.writeText(
		stanzaData.rows.map((row) => row.line).join("\n"),
	);
}

loadStanza();
