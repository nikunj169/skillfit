const languages = [
  { value: "en", label: "English" },
  { value: "hi", label: "Hindi" },
  { value: "kn", label: "Kannada" },
];

function LanguageToggle({ value, onChange }) {
  return (
    <div className="toggle-row">
      {languages.map((language) => (
        <button
          key={language.value}
          type="button"
          className={value === language.value ? "chip chip-active" : "chip"}
          onClick={() => onChange(language.value)}
        >
          {language.label}
        </button>
      ))}
    </div>
  );
}

export default LanguageToggle;
