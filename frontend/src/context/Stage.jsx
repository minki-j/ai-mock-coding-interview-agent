import { useState } from 'react';
import { StageContext } from './StageContext';
import PropTypes from 'prop-types';

export function StageProvider({ children }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [nextStep, setNextStep] = useState(0);
  const [didUserConfirm, setDidUserConfirm] = useState(true);

  const value = {
    currentStep,
    setCurrentStep,
    nextStep,
    setNextStep,
    didUserConfirm,
    setDidUserConfirm,
  };

  return (
    <StageContext.Provider value={value}>
      {children}
    </StageContext.Provider>
  );
}

StageProvider.propTypes = {
  children: PropTypes.node.isRequired,
};
