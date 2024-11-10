import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import PythonEditor from "../components/PythonEditor";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import ChatContainer from "../components/ChatContainer";
import messageSound from "../assets/sounds/message-pop-alert.mp3";

const Interview = () => {
  const { id } = useParams();
  const [interviewQuestion, setInterviewQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [code, setCode] = useState("");
  const [testResult, setTestResult] = useState(
    "Once you run the code, you will see the results here."
  );
  const [isQuestionsVisible, setIsQuestionsVisible] = useState(true);
  const [isEditorVisible, setIsEditorVisible] = useState(true);
  const [isResultsVisible, setIsResultsVisible] = useState(true);

  const executeCode = async () => {
    setTestResult("Running code...");
    try {
      const response = await fetch("/execute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code: code,
          timeout: 5000,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setTestResult(data.output || data.error || "No output");
      } else {
        const errorData = await response.json();
        setTestResult(`Error: ${errorData.detail || "Failed to execute code"}`);
      }
    } catch (error) {
      setTestResult(`Error: ${error.message}`);
    }
  };

  useEffect(() => {
    console.log("fetching interview with id", id);
    const fetchInterview = async () => {
      try {
        const res = await fetch(`/get_interview/${id}`);
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();
        setMessages(data.messages || []);
        setCode(data.code_editor_state || code);
        if (data.test_result) {
          setTestResult(data.test_result);
        }
        setInterviewQuestion(data.interview_question || "");
      } catch (error) {
        console.error("Error fetching interview:", error);
      }
    };
    fetchInterview();
  }, []);

  const handleSendMessage = async (message) => {
    const userMessage = {
      message: message,
      sentTime: new Date().toISOString(),
      sender: "User",
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
          interview_id: id,
          code_editor_state: code,
          test_result: testResult,
        }),
      });
      const message_from_interviewer = await response.json();
      const interviewerMessage = {
        message: message_from_interviewer,
        sentTime: new Date().toISOString(),
        sender: "AI",
      };

      // Use a timeout to ensure the sound plays after the message is added
      setTimeout(() => {
        setMessages((prevMessages) => [...prevMessages, interviewerMessage]);
        const audio = new Audio(messageSound);
        audio.play(); // Play sound when interviewer responds
      }, 100);
    } catch (error) {
      console.error("Error handling chat response:", error);
      // Optionally handle the error in the UI
    }
  };

  const handleFinalSolutionSubmit = async (e) => {
    e.preventDefault();
    console.log("Code submitted:", code);
    // Here you can handle the code submission logic
  };

  return (
    <div className="container h-[calc(100vh-120px)] max-w-full">
      <div className="grid grid-cols-2 gap-2.5 h-full">
        {/* Left Column with Questions and Chat */}
        <div className="col-span-1 flex flex-col gap-2.5 h-full overflow-hidden">
          {/* Interview Questions Section */}
          <div
            className={`flex-initial px-4 py-2 bg-white border border-gray-100 rounded-lg shadow-inner ${
              isQuestionsVisible ? "h-[432px]" : "h-[40px]"
            }`}
          >
            <div
              className="flex gap-2 items-center cursor-pointer"
              onClick={() => setIsQuestionsVisible(!isQuestionsVisible)}
            >
              <span>{isQuestionsVisible ? "▼" : "▶"}</span>
              <h2 className="font-semibold">Interview Question</h2>
            </div>
            {isQuestionsVisible && (
              <div className="mt-2">
                <div
                  className="h-[370px] overflow-y-auto prose prose-sm max-w-none pb-4"
                  dangerouslySetInnerHTML={{ __html: interviewQuestion }}
                ></div>
              </div>
            )}
          </div>

          {/* Chat UI Kit Section */}
          <div className="flex-1 overflow-y-auto">
            <ChatContainer
              messages={messages}
              onSendMessage={handleSendMessage}
            />
          </div>
        </div>

        {/* Right Column - Code Editor (unchanged) */}
        <div className="col-span-1 flex flex-col gap-2.5 h-full">
          {/* Code Editor Section */}
          <div
            className={`rounded bg-white border border-gray-100 shadow-inner p-5 flex-1 ${
              isEditorVisible ? "h-[432px]" : "h-[40px]"
            }`}
          >
            <div
              className="flex gap-2 items-center cursor-pointer"
              onClick={() => setIsEditorVisible(!isEditorVisible)}
            >
              <span>{isEditorVisible ? "▼" : "▶"}</span>
              <h2 className="font-semibold">Code Editor</h2>
            </div>
            {isEditorVisible && (
              <PythonEditor
                code={code}
                setCode={setCode}
                testResult={testResult}
                executeCode={executeCode}
              />
            )}
          </div>
          <div
            className={`mt-8 border border-gray-200 rounded-lg p-5 ${
              isResultsVisible ? "h-[200px]" : "h-[40px]"
            }`}
          >
            <div
              className="flex gap-2 items-center cursor-pointer"
              onClick={() => setIsResultsVisible(!isResultsVisible)}
            >
              <span>{isResultsVisible ? "▼" : "▶"}</span>
              <h2 className="font-semibold">Test Results</h2>
            </div>
            {isResultsVisible && <div className="mt-2">{testResult}</div>}
          </div>
          {/* Submit Button Section */}
          <div className="flex gap-2.5 w-full">
            <button
              className="flex-1 px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-800"
              onClick={handleFinalSolutionSubmit}
            >
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Interview;
