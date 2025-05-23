import { useContext } from "react";
import { StageContext } from "../context/StageContext";

const ProgressTracker = () => {
  const { currentStep, setCurrentStep } = useContext(StageContext);

  const pathname = window.location.pathname;
  const id = pathname.split("/interview/")[1];
  
  const steps = [
    { id: 0, label: "Thought process", code: "thought_process" },
    { id: 1, label: "Coding", code: "coding" },
    { id: 2, label: "Debugging", code: "debugging" },
    { id: 3, label: "Algorithmic analysis", code: "algorithmic_analysis" },
    { id: 4, label: "Submission", code: "assessment" },
  ];

  const handleStepClick = async (step) => {
    const currentStepIndex = steps.findIndex((s) => s.code === currentStep);
    const clickedStepIndex = steps.findIndex((s) => s.code === step);

    // Check if trying to skip more than one step forward
    if (
      clickedStepIndex > currentStepIndex + 1 ||
      clickedStepIndex < currentStepIndex - 1
    ) {
      alert("You can only move 1 step at a time!");
      return;
    }

    const response = await fetch("/change_step", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        interview_id: id,
        step: step,
      }),
    });
    if (response.ok) {
      console.log("Step changed to", step);
      setCurrentStep(step);
    } else {
      console.error("Failed to change step");
    }
  };
  
  const chevronStyle = {
    clipPath:
      "polygon(0 0, calc(100% - 10px) 0, 100% 50%, calc(100% - 10px) 100%, 0 100%, 10px 50%)",
  };
  
  return (
    <div className="container mx-auto px-4 py-6">
      <div className="flex justify-center">
        {steps.map((step) => (
          <div key={step.id} className="relative flex items-center h-10">
            <div
              style={chevronStyle}
              onClick={() => handleStepClick(step.code)}
              title="Click to move step"
              className={`flex items-center justify-center px-6 h-full hover:cursor-pointer 
                transform transition-transform duration-100 hover:-translate-y-1
                ${
                  step.id < steps.findIndex((step) => step.code === currentStep)
                    ? "bg-blue-600 text-white"
                    : step.id ===
                      steps.findIndex((step) => step.code === currentStep)
                    ? "bg-green-300 text-black"
                    : "bg-gray-100 text-gray-500"
                }`}
            >
              <span className="text-sm whitespace-nowrap">
                {step.id <
                  steps.findIndex((step) => step.code === currentStep) && "✓ "}
                {step.label}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProgressTracker;
