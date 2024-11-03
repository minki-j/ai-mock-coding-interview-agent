import { useState } from "react";

import CodeEditor from "@uiw/react-textarea-code-editor";

const PythonEditor = () => {
  const [code, setCode] = useState(`def function(name):
  print(name)

function("hello world")`);

  const handleSubmit = async (e) => {
    e.preventDefault();
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="flex flex-col gap-2.5">
        <div className="border border-gray-200 rounded-lg">
          <CodeEditor
            value={code}
            language="python"
            placeholder="Please enter Python code."
            onChange={(evn) => setCode(evn.target.value)}
            padding={15}
            style={{
              backgroundColor: "#f5f5f5",
              fontFamily:
                "ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace",
            }}
          />
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Run
        </button>
      </form>
      <div className="mt-8 border border-gray-200 rounded-lg p-5">
        <h4 className="text-lg font-semibold mb-2">Output</h4>
        <p id="output_content"></p>
      </div>
    </div>
  );
};

export default PythonEditor;
