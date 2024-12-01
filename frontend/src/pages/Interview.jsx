import { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import { useContext } from "react";
import { StageContext } from "../context/StageContext";
import ChatContainer from "../components/ChatContainer";
import PythonEditor from "../components/PythonEditor";
import messageSound from "../assets/sounds/message-pop-alert.mp3";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";

const Interview = () => {
  const { id } = useParams();
  const [interviewQuestion, setInterviewQuestion] = useState("");
  const [interviewTitle, setInterviewTitle] = useState("");
  const [messages, setMessages] = useState([]);
  const [code, setCode] = useState("");
  const [testCode, setTestCode] = useState("");
  const [testResult, setTestResult] = useState("");
  const [isQuestionsVisible, setIsQuestionsVisible] = useState(true);
  const [isEditorVisible, setIsEditorVisible] = useState(true);
  const [isResultsVisible, setIsResultsVisible] = useState(true);
  const isFirstRender = useRef(true);
  const skipNextCodeEditorUpdate = useRef(false);
  const {
    currentStep,
    setCurrentStep,
    didUserConfirm,
    setDidUserConfirm,
    // showUserConfirmation,
    setShowUserConfirmation,
    // nextStep,
    setNextStep,
  } = useContext(StageContext);
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
    setDidUserConfirm(true);
    setShowUserConfirmation(false);

    const fetchInterview = async () => {
      try {
        const res = await fetch(`/get_interview/${id}`);
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();

        if (data.messages && data.messages.length > 1) {
          setMessages(data.messages);
        } else {
          setTimeout(() => {
            setMessages(data.messages || []);
            const audio = new Audio(messageSound);
            audio.play();
          }, 2000);
        }

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
        setInterviewTitle(data.interview_title || "");
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
    if (message) {
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          message: message,
          sentTime: new Date().toISOString(),
          sender: "User",
        },
      ]);
    }

    try {
      let allDecisionsCompleted = false;
      let isFirstFetchDone = false;
      let finalResponse = "";

      // To receive Agent's inner process messages(display_decision), we need to call the chat endpoint multiple times until the graph is reached the end.
      while (!allDecisionsCompleted) {
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
            wait_for_user_confirmation: !didUserConfirm,
            is_first_fetch_done: isFirstFetchDone,
          }),
        });
        isFirstFetchDone = true;

        const data = await response.json();

        if (!data) {
          // If the response is empty, we need show the user confirmation button, and quit this handleSendMessage function.
          setTimeout(() => {
            setShowUserConfirmation(true);
          }, 1500);
          return;
        }

        if (!data.display_decision) {
          // If display_decision is empty, it means that the graph is reached the end. Break the while loop by setting allDecisionsCompleted to true and pass the data to finalResponse
          allDecisionsCompleted = true;
          finalResponse = data;
        } else {
          // If display_decision is not empty, it means that the graph is interrupted. We need to display the message.
          setMessages((prevMessages) => [
            ...prevMessages,
            {
              message: data.display_decision,
              sentTime: new Date().toISOString(),
              sender: "display_decision",
            },
          ]);
        }
      }

      // Handle the stage change
      let new_step = finalResponse.stage;
      if (new_step === "main") {
        new_step = finalResponse.main_stage_step;
      }
      if (new_step !== currentStep && currentStep !== "greeting" && new_step !== "assessment") {
        setDidUserConfirm(false);
        setNextStep(new_step);
      }
      if (currentStep == "greeting") {
        setCurrentStep(new_step);
      }

      // Display the message from the interviewer
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            message: finalResponse.message_from_interviewer,
            sentTime: new Date().toISOString(),
            sender: "AI",
          },
        ]);
        const audio = new Audio(messageSound);
        audio.play();
      }, 100);
    } catch (error) {
      console.error("Error handling chat response:", error);
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
              title="Click to collapse or expand"
              onClick={() => setIsQuestionsVisible(!isQuestionsVisible)}
            >
              <span>{isQuestionsVisible ? "▼" : "▶"}</span>
              <h2 className="font-semibold">{interviewTitle}</h2>
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
              setMessages={setMessages}
              onSendMessage={handleSendMessage}
              handleSendMessage={handleSendMessage}
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
              title="Click to collapse or expand"
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
              title="Click to collapse or expand"
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

Interview.propTypes = {};

export default Interview;
