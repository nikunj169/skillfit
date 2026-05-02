import { useEffect, useState } from "react";

function AIVoicePrompt({ question, language }) {
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    window.speechSynthesis.cancel();
    setIsPlaying(false);
    return () => {
      window.speechSynthesis.cancel();
    };
  }, [question]);

  const handlePlay = () => {
    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(question);
    
    if (language === "kn") utterance.lang = "kn-IN";
    else if (language === "hi") utterance.lang = "hi-IN";
    else utterance.lang = "en-US";
    
    utterance.onend = () => setIsPlaying(false);
    utterance.onerror = () => setIsPlaying(false);
    
    window.speechSynthesis.speak(utterance);
    setIsPlaying(true);
  };

  return (
    <section className="panel panel-soft">
      <p className="section-kicker">AI Prompt</p>
      <h3>{question}</h3>
      <div className="button-row" style={{ marginTop: "16px" }}>
        <button type="button" className="button button-secondary" onClick={handlePlay}>
          {isPlaying ? "Stop Audio" : "Play Question"}
        </button>
      </div>
    </section>
  );
}

export default AIVoicePrompt;
