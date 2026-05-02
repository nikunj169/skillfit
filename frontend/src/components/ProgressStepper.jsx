function ProgressStepper({ currentStep, totalSteps }) {
  return (
    <div className="stepper">
      {Array.from({ length: totalSteps }).map((_, index) => {
        const step = index + 1;
        const className =
          step < currentStep ? "step step-complete" : step === currentStep ? "step step-active" : "step";
        return (
          <div key={step} className={className}>
            <span>{step}</span>
          </div>
        );
      })}
    </div>
  );
}

export default ProgressStepper;
