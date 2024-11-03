import PropTypes from "prop-types";
import CodeEditor from "@uiw/react-textarea-code-editor";

const PythonEditor = ({ code, setCode, testResult, executeCode }) => {
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
        <div>{testResult}</div>
      </div>
    </div>
  );
};

PythonEditor.propTypes = {
  code: PropTypes.string.isRequired,
  setCode: PropTypes.func.isRequired,
  testResult: PropTypes.string.isRequired,
  executeCode: PropTypes.func.isRequired,
};

export default PythonEditor;
