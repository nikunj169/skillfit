import { useCallback, useEffect, useRef, useState } from "react";

export function useMediaRecorder() {
  const [permissionState, setPermissionState] = useState("idle");
  const [isRecording, setIsRecording] = useState(false);
  const [stream, setStream] = useState(null);
  const [mediaError, setMediaError] = useState("");
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    streamRef.current = stream;
  }, [stream]);

  const requestPermissions = useCallback(async (keepAlive = false) => {
    try {
      setMediaError("");

      if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error("Camera and microphone are not supported by this browser.");
      }

      const newStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } },
        audio: { echoCancellation: true, noiseSuppression: true },
      });

      if (!keepAlive) {
        newStream.getTracks().forEach((track) => track.stop());
      } else {
        streamRef.current?.getTracks().forEach((track) => track.stop());
        streamRef.current = newStream;
        setStream(newStream);
      }

      setPermissionState("granted");
      return true;
    } catch (error) {
      setMediaError(error?.message || "Camera or microphone permission failed.");
      setPermissionState("denied");
      return false;
    }
  }, []);

  const startRecording = useCallback(() => {
    const activeStream = streamRef.current;
    if (!activeStream) return null;

    let mediaRecorder;
    try {
      const mimeType = MediaRecorder.isTypeSupported("video/webm;codecs=vp8,opus")
        ? "video/webm;codecs=vp8,opus"
        : "video/webm";
      mediaRecorder = new MediaRecorder(activeStream, { mimeType });
    } catch {
      mediaRecorder = new MediaRecorder(activeStream);
    }

    mediaRecorderRef.current = mediaRecorder;

    const chunks = [];
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) chunks.push(event.data);
    };

    return new Promise((resolve) => {
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: mediaRecorder.mimeType || "video/webm" });
        resolve(blob);
      };
      mediaRecorder.start();
      setIsRecording(true);
    });
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, []);

  const cleanupStream = useCallback(() => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    setStream(null);
  }, []);

  return {
    permissionState,
    mediaError,
    requestPermissions,
    startRecording,
    stopRecording,
    cleanupStream,
    isRecording,
    stream,
  };
}
