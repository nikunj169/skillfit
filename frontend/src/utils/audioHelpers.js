export function buildPromptText(question, language) {
  return `${language.toUpperCase()} prompt: ${question}`;
}
