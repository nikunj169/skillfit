import { buildPromptText } from "../utils/audioHelpers";

function AIVoicePrompt({ question, language }) {
  return (
    <section className="panel panel-soft">
      <p className="section-kicker">AI Prompt</p>
      <h3>{question}</h3>
      <p>{buildPromptText(question, language)}</p>
    </section>
  );
}

export default AIVoicePrompt;
