import { useState } from "react";

import CodeEditor from "@uiw/react-textarea-code-editor";


const PythonEditor = () => {
  const [code, setCode] = useState(`def greet(name):
  print("Hello, " + name)

greet("Minki")`);
  const [testResults, setTestResults] = useState('');

  const executeCode = async () => {
    setTestResults('Running code...');
    try {
      const response = await fetch('http://localhost:8000/execute-code', {
        method: 'POST',
      body: JSON.stringify({ code }),
    });
    if (response.ok) {
      const data = await response.json();
      setTestResults(data.output);
    } else {
        setTestResults('Error executing code');
      }
    } catch (error) {
      setTestResults(`Error: ${error.message}`);
    }
  };

  return (
    <div>
      <div className="flex flex-col gap-2.5">
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
          onClick={executeCode}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Run
        </button>
      </div>
      <div className="mt-8 border border-gray-200 rounded-lg p-5">
        <h4 className="text-lg font-semibold mb-2">Test Results</h4>
        <div>{testResults}</div>
      </div>
    </div>
  );
};

export default PythonEditor;
