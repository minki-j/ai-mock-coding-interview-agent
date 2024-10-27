from fasthtml.common import *


#! Styling is not working. I've tested in a pure HTML and it works fine. I think FastHTML is messing with it.
def python_editor():
    return (
        Div(
            Form(
                hx_post="/run_python",
                hx_target="#output_content",
                hx_swap="innerHTML",
                style="display: flex; flex-direction: column; gap: 10px;",
            )(
                Div()(
                    Textarea(
                        id="code_editor",
                        name="code",
                        placeholder="Write your code here...",
                    ),
                ),
                Button(type="submit")("Run"),
            ),
            Div(
                id="output_div",
                style="margin-top: 30px;  border: 1px solid #ddd; border-radius: 8px; padding: 20px;",
            )(
                H4("Output"),
                P(id="output_content"),
            ),
        ),
    )


# TODO: Code mirror is not styled properly in FastHTML. We are going to use a simple textarea tag for now.

#                 Script(
#                     src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/codemirror.min.js"
#                 ),
#                 Script(
#                     src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/mode/python/python.min.js"
#                 ),
#                 Script(src="https://cdn.jsdelivr.net/pyodide/v0.18.1/full/pyodide.js"),
#                 Script(
#                     """
# let editor = CodeMirror.fromTextArea(document.getElementById("code_editor"), {
#   mode: "python",
#   lineNumbers: true,
# });
# async function runPython() {
#   let pyodide = await loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/" });
#   return pyodide;
# }
# let pyodideReadyPromise = runPython();
# async function evaluatePython() {
#   let pyodide = await pyodideReadyPromise;
#   try {
#     let result = pyodide.runPython(editor.getValue());
#     document.getElementById("output").innerText = result;
#   } catch (error) {
#     document.getElementById("output").innerText = "Error: " + error.message;
#   }
# }
#         """
#                 ),
