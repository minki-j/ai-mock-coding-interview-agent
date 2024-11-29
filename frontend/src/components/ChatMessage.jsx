import PropTypes from "prop-types";
import { useState } from "react";
import { useContext } from "react";
import { StageContext } from "../context/StageContext";
import { useParams } from "react-router-dom";
const ChatMessage = ({ role, content}) => {
  const { id } = useParams();
  const { setDidUserConfirm, didUserConfirm, setCurrentStep, nextStep } =
    useContext(StageContext);
  const [showButtons, setShowButtons] = useState(!didUserConfirm);

  const handleResponse = async (accepted) => {
    setShowButtons(false);
    if (accepted) {
      setCurrentStep(nextStep);      
      setDidUserConfirm(true);
    } else {
      try {
        fetch("/revert_stage", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            interview_id: id,
          }),
        }).then((res) => {
          if (res.ok) {
            console.log("Stage reverted");
          setDidUserConfirm(true);
        } else {
            console.error("Failed to revert stage");
          }
        });
      } catch (error) {
        console.error("Error reverting stage:", error);
      }
    }
  };

  return (
    <div
      className={`flex flex-col ${
        role === "User" ? "items-end" : "items-start"
      } w-full`}
    >
      <div
        className={`mt-2 mb-2 p-2 border border-gray-200 rounded-xl max-w-[70%] w-fit relative shadow-sm ${
          role === "User" ? "ml-auto bg-blue-200" : "mr-auto"
        }`}
      >
        <p>{content}</p>
      </div>
      {showButtons && role === "AI" && (
        <div className="mt-0 mb-3 p-2 border border-gray-200 rounded-xl w-fit relative shadow-md">
          <p>
            I believe you&apos;re ready to move to the next stage. Shall we proceed?
          </p>
          <div
            className={`flex gap-2 mt-2 ${
              role === "User" ? "justify-end" : "justify-start"
            }`}
          >
            <button
              onClick={() => handleResponse(true)}
              className="px-2 py-1 bg-blue-400 text-white rounded hover:bg-blue-500 text-sm"
            >
              Yes, continue
            </button>
            <button
              onClick={() => handleResponse(false)}
              className="px-2 py-1 border border-gray-200 text-gray-500 rounded hover:bg-gray-100 text-sm"
            >
              No, not yet
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

ChatMessage.propTypes = {
  role: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired,
};

export default ChatMessage;
