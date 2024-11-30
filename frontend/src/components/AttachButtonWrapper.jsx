import { Button } from "@chatscope/chat-ui-kit-react";

export const AttachButtonWrapper = (props) => {
  return (
    <Button
      {...props} 
      icon={<span className="material-symbols-outlined">mic</span>}
    />
  );
};
