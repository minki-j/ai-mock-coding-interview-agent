from fasthtml.common import *

#! Styling is not working. I've tested in a pure HTML and it works fine. I think FastHTML is messing with it.
def python_editor():
    return (
        Div(
            Div(style="display: flex; flex-direction: column; gap: 10px;")(
                Div()(
                    Textarea(id="code_editor"),
                ),
                Button("Run", onclick="evaluatePython()"),
                Script(
                    src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/codemirror.min.js"
                ),
                Script(
                    src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/mode/python/python.min.js"
                ),
                Script(src="https://cdn.jsdelivr.net/pyodide/v0.18.1/full/pyodide.js"),
                Script(
                    """
let editor = CodeMirror.fromTextArea(document.getElementById("code_editor"), {
  mode: "python",
  lineNumbers: true,
});

async function runPython() {
  let pyodide = await loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/" });
  return pyodide;
}

let pyodideReadyPromise = runPython();

async function evaluatePython() {
  let pyodide = await pyodideReadyPromise;
  try {
    let result = pyodide.runPython(editor.getValue());
    document.getElementById("output").innerText = result;
  } catch (error) {
    document.getElementById("output").innerText = "Error: " + error.message;
  }
}
        """
                ),
            ),
            Div(id="output")(P("Output")),
        ),
    )
