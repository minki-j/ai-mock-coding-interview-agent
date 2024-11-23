import PropTypes from 'prop-types';

const ProgressTracker = ({ currentStep }) => {
  const steps = [
    { id: 1, label: "Thought process" },
    { id: 2, label: "Coding" },
    { id: 3, label: "Debugging" },
    { id: 4, label: "Algorithmic analysis" },
    { id: 5, label: "Submission" },
  ];

  // Find the current step index
  const currentStepIndex = steps.findIndex(step => step.label === currentStep) + 1;

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
              className={`flex items-center justify-center px-6 h-full
                ${
                  step.id < currentStepIndex
                    ? "bg-blue-600 text-white"
                    : step.id === currentStepIndex
                    ? "bg-green-300 text-black"
                    : "bg-gray-100 text-gray-500"
                }`}
            >
              <span className="text-sm whitespace-nowrap">
                {step.id < currentStepIndex && "✓ "}
                {step.label}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

ProgressTracker.propTypes = {
  currentStep: PropTypes.string.isRequired,
};

export default ProgressTracker;
