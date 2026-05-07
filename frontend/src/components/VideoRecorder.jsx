import { useEffect, useMemo, useRef, useState } from "react";

function getCameraStatus(stream, playbackError) {
  if (playbackError) return playbackError;
  if (!stream) return "Starting camera preview...";

  const [videoTrack] = stream.getVideoTracks();
  if (!videoTrack) return "No camera video track was found.";
  if (videoTrack.readyState !== "live") return "Camera stream is not live. Refresh and allow camera access again.";
  if (videoTrack.muted) return "Camera is connected, but the video track is muted.";

  return "";
}

function VideoRecorder({ stream, isRecording, onStart, onStop, disabled, mediaError }) {
  const videoRef = useRef(null);
  const [playbackError, setPlaybackError] = useState("");
  const [hasVideoFrame, setHasVideoFrame] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    setHasVideoFrame(false);
    setPlaybackError("");

    if (!stream) {
      video.srcObject = null;
      return;
    }

    video.srcObject = stream;
    video.muted = true;
    video.playsInline = true;

    const playPreview = async () => {
      try {
        await video.play();
      } catch (error) {
        setPlaybackError(error?.message || "Camera preview could not start.");
      }
    };

    if (video.readyState >= 2) {
      playPreview();
    } else {
      video.onloadedmetadata = playPreview;
    }

    return () => {
      video.onloadedmetadata = null;
    };
  }, [stream]);

  const statusMessage = useMemo(
    () => mediaError || getCameraStatus(stream, playbackError),
    [mediaError, playbackError, stream],
  );

  return (
    <div className="form-field">
      <div style={{ position: "relative" }}>
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          onLoadedData={() => setHasVideoFrame(true)}
          style={{
            width: "100%",
            borderRadius: "16px",
            background: "#000",
            minHeight: "240px",
            objectFit: "cover",
            display: "block",
          }}
        />

        {statusMessage && !hasVideoFrame && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: "20px",
              textAlign: "center",
              color: "rgba(255,255,255,0.82)",
              background: "rgba(0,0,0,0.56)",
              borderRadius: "16px",
              fontSize: "0.95rem",
              lineHeight: 1.5,
            }}
          >
            {statusMessage}
          </div>
        )}

        {isRecording && (
          <div
            style={{
              position: "absolute",
              top: "12px",
              left: "12px",
              display: "flex",
              alignItems: "center",
              gap: "6px",
              background: "rgba(0,0,0,0.6)",
              padding: "4px 10px",
              borderRadius: "99px",
            }}
          >
            <span
              style={{
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                background: "#ef4444",
              }}
            />
            <span style={{ fontSize: "0.75rem", color: "#fff", fontWeight: 600 }}>REC</span>
          </div>
        )}
      </div>

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
