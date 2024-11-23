import { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import PropTypes from "prop-types";
import PythonEditor from "../components/PythonEditor";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import ChatContainer from "../components/ChatContainer";
import messageSound from "../assets/sounds/message-pop-alert.mp3";

const Interview = ({ setCurrentStep }) => {
  const { id } = useParams();
  const [interviewQuestion, setInterviewQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [code, setCode] = useState("");
  const [testCode, setTestCode] = useState("");
  const [testResult, setTestResult] = useState("");
  const [isQuestionsVisible, setIsQuestionsVisible] = useState(true);
  const [isEditorVisible, setIsEditorVisible] = useState(true);
  const [isResultsVisible, setIsResultsVisible] = useState(true);
  const isFirstRender = useRef(true);
  const skipNextCodeEditorUpdate = useRef(false);

  const default_imports =
    "from typing import List, Tuple, Dict, Set, Optional, Any, Union, Callable\n\n";
  const executeCode = async () => {
    setTestResult("Running code...");
    try {
      const response = await fetch("/execute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code: default_imports + code + "\n\n" + testCode,
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
        setCode(
          data.code_editor_state === ""
            ? data.code_snippet[0]["code"]
            : data.code_editor_state
        );
        setTestCode(data.test_code);
        if (data.test_result) {
          setTestResult(data.test_result);
        }
        setInterviewQuestion(data.interview_question || "");
        let current_step = data.stage;
        if (current_step === "main") {
          current_step = data.main_stage_step;
        }
        setCurrentStep(current_step);
        skipNextCodeEditorUpdate.current = true;
      } catch (error) {
        console.error("Error fetching interview:", error);
      }
    };
    fetchInterview();
  }, [id]);

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
      const data = await response.json();
      const message_from_interviewer = data.message_from_interviewer;
      const interviewerMessage = {
        message: message_from_interviewer,
        sentTime: new Date().toISOString(),
        sender: "AI",
      };

      let current_step = data.stage;
      if (current_step === "main") {
        current_step = data.main_stage_step;
      }
      current_step = current_step.charAt(0).toUpperCase() + current_step.slice(1).replace("_", " ");
      setCurrentStep(current_step);

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

  useEffect(() => {
    if (skipNextCodeEditorUpdate.current) {
      skipNextCodeEditorUpdate.current = false;
      return;
    }

    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }

    if (code.length === 0 && testResult.length === 0) {
      return;
    }

    const timeoutId = setTimeout(() => {
      const handleUpdateCodeEditorState = async () => {
        await fetch("/update_code_editor_state", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            interview_id: id,
            code_editor_state: code,
            test_result: testResult,
          }),
        });
      };
      handleUpdateCodeEditorState();
    }, 5000);

    return () => clearTimeout(timeoutId);
  }, [code, testResult]);

  return (
    <div className="container h-[calc(100vh-200px)] max-w-full">
      <div className="grid grid-cols-2 gap-2.5 h-full">
        {/* Left Column with Questions and Chat */}
        <div className="col-span-1 flex flex-col gap-2.5 h-full overflow-hidden">
          {/* Interview Questions Section */}
          <div
            className={`flex-initial bg-white border border-gray-100 rounded-lg shadow-inner p-5 ${
              isQuestionsVisible ? "flex-1" : "h-[60px]"
            } ${!isQuestionsVisible && !messages.length ? "flex-1" : ""}`}
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
          <div
            className={`${
              isQuestionsVisible ? "flex-1" : "flex-[2]"
            } overflow-y-auto`}
          >
            <ChatContainer
              messages={messages}
              onSendMessage={handleSendMessage}
            />
          </div>
        </div>

        {/* Right Column */}
        <div className="col-span-1 flex flex-col gap-2.5 h-full overflow-hidden">
          {/* Code Editor Section */}
          <div
            className={`bg-white border border-gray-100 shadow-inner p-5 overflow-y-auto ${
              isEditorVisible ? "flex-1" : "h-[60px]"
            } ${!isEditorVisible && !isResultsVisible ? "flex-1" : ""}`}
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

          {/* Test Results Section */}
          <div
            className={`border border-gray-200 rounded-lg p-5 overflow-x-auto overflow-y-auto ${
              isResultsVisible ? "flex-1" : "h-[60px]"
            } ${!isEditorVisible && isResultsVisible ? "flex-[2]" : ""}`}
          >
            <div
              className="flex gap-2 items-center cursor-pointer"
              onClick={() => setIsResultsVisible(!isResultsVisible)}
            >
              <span>{isResultsVisible ? "▼" : "▶"}</span>
              <h2 className="font-semibold">Test Results</h2>
            </div>
            {isResultsVisible && (
              <div className="mt-2 p-5 h-full">{testResult}</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

Interview.propTypes = {
  setCurrentStep: PropTypes.func.isRequired,
};

export default Interview;
