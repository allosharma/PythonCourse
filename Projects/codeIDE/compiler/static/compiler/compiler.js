const body = document.body;
const runButton = document.getElementById("run-btn");
const sampleButton = document.getElementById("sample-btn");
const clearOutputButton = document.getElementById("clear-output-btn");
const codeEditor = document.getElementById("code-editor");
const stdinEditor = document.getElementById("stdin-editor");
const outputConsole = document.getElementById("output-console");
const statusPill = document.getElementById("status-pill");
const durationPill = document.getElementById("duration-pill");
const starterCode = JSON.parse(document.getElementById("starter-code").textContent);

function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split("; ") : [];
    for (const cookie of cookies) {
        const [cookieName, ...rest] = cookie.split("=");
        if (cookieName === name) {
            return decodeURIComponent(rest.join("="));
        }
    }
    return "";
}

function setStatus(state, label) {
    statusPill.dataset.state = state;
    statusPill.textContent = label;
}

function renderOutput(message) {
    outputConsole.textContent = message;
}

function buildConsoleText(payload) {
    const sections = [];

    if (payload.stdout) {
        sections.push(payload.stdout.trimEnd());
    }

    if (payload.stderr) {
        sections.push(payload.stderr.trimEnd());
    }

    if (!sections.length) {
        sections.push("Program finished with no output.");
    }

    return sections.join("\n\n====================\n\n");
}

async function runCode() {
    const sourceCode = codeEditor.value;

    if (!sourceCode.trim()) {
        setStatus("error", "Missing code");
        durationPill.textContent = "0 ms";
        renderOutput("Write some Python before running the compiler.");
        return;
    }

    runButton.disabled = true;
    setStatus("running", "Running");
    durationPill.textContent = "Working...";
    renderOutput("Executing Python in a separate process...");

    try {
        const response = await fetch(body.dataset.runUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({
                code: sourceCode,
                stdin: stdinEditor.value,
            }),
        });

        const payload = await response.json();
        if (!response.ok) {
            throw new Error(payload.message || "The compiler request failed.");
        }

        setStatus(payload.ok ? "success" : "error", payload.ok ? "Success" : "Finished with errors");
        durationPill.textContent = `${payload.duration_ms} ms`;
        renderOutput(buildConsoleText(payload));
    } catch (error) {
        setStatus("error", "Request failed");
        durationPill.textContent = "0 ms";
        renderOutput(error.message || "Unable to run the compiler right now.");
    } finally {
        runButton.disabled = false;
    }
}

runButton.addEventListener("click", runCode);

sampleButton.addEventListener("click", () => {
    codeEditor.value = starterCode;
    setStatus("idle", "Ready");
    durationPill.textContent = "0 ms";
    renderOutput('Sample Python restored. Press "Run code" to execute your script.');
    codeEditor.focus();
});

clearOutputButton.addEventListener("click", () => {
    setStatus("idle", "Ready");
    durationPill.textContent = "0 ms";
    renderOutput("Console cleared.");
});

codeEditor.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        runCode();
    }
});
