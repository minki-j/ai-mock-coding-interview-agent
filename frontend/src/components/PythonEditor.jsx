import PropTypes from "prop-types";
import CodeEditor from "@uiw/react-textarea-code-editor";

const PythonEditor = ({ code, setCode, executeCode }) => {
  return (
    <div className="relative" >
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
          className="absolute top-3.5 right-4 w-10 h-10 rounded-full bg-blue-400 hover:bg-blue-500 text-white flex items-center justify-center transition-all duration-200 shadow-md hover:shadow-lg"
        >
          <div className="w-0 h-0 border-t-[8px] border-t-transparent border-l-[12px] border-l-white border-b-[8px] border-b-transparent ml-1" />
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
