import PropTypes from "prop-types";
import CodeEditor from "@uiw/react-textarea-code-editor";

const PythonEditor = ({ code, setCode, executeCode }) => {
  return (
    <div className="relative">
      <div className="flex flex-col gap-2.5">
        <div className="border border-gray-200 rounded-lg">
          <CodeEditor
            value={code}
            language="python"
            placeholder="Please enter Python code."
            onChange={(evn) => setCode(evn.target.value)}
            padding={15}
            data-color-mode="light"
            style={{
              backgroundColor: "#f5f5f5",
              fontSize: "16px",
              fontFamily:
                "ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace",
            }}
          />
        </div>
        <button
          onClick={executeCode}
          className="absolute bottom-2 right-2 w-10 h-7 rounded-lg bg-blue-400 hover:bg-blue-500 text-white flex items-center justify-center transition-all duration-100 shadow-md hover:shadow-lg text-xs"
        >
          Run
        </button>
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
