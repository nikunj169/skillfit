import { useEffect, useRef } from "react";

function VideoRecorder({ stream, isRecording, onStart, onStop, disabled }) {
  const videoRef = useRef(null);

  useEffect(() => {
    if (videoRef.current && stream) {
      videoRef.current.srcObject = stream;
    }
  }, [stream]);

  return (
    <div className="form-field">
      <video 
        ref={videoRef} 
        autoPlay 
        muted 
        playsInline
        style={{ width: "100%", borderRadius: "16px", background: "#000", minHeight: "240px", objectFit: "cover" }}
      />
      <div className="button-row" style={{ marginTop: "12px", justifyContent: "center" }}>
        {!isRecording ? (
          <button type="button" className="button button-primary" onClick={onStart} disabled={disabled || !stream}>
            Start Recording
          </button>
        ) : (
          <button type="button" className="button button-secondary" onClick={onStop} disabled={disabled}>
            Stop Recording
          </button>
        )}
      </div>
    </div>
  );
}

export default VideoRecorder;
