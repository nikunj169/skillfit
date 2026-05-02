function VideoRecorder({ responseText, onChange, disabled }) {
  return (
    <label className="form-field">
      <span>Your response transcript</span>
      <textarea
        rows="6"
        value={responseText}
        onChange={(event) => onChange(event.target.value)}
        placeholder="For now this starter app submits transcript text while the media pipeline is being built."
        disabled={disabled}
      />
    </label>
  );
}

export default VideoRecorder;
