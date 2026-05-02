import { useState, useRef, useCallback } from "react";

export function useMediaRecorder() {
  const [permissionState, setPermissionState] = useState("idle");
  const [isRecording, setIsRecording] = useState(false);
  const [stream, setStream] = useState(null);
  const mediaRecorderRef = useRef(null);

  const requestPermissions = useCallback(async (keepAlive = false) => {
    try {
      if (navigator.mediaDevices?.getUserMedia) {
        const newStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        if (!keepAlive) {
          newStream.getTracks().forEach((track) => track.stop());
        } else {
          setStream(newStream);
        }
      }
      setPermissionState("granted");
      return true;
    } catch {
      setPermissionState("denied");
      return false;
    }
  }, []);

  const startRecording = useCallback(() => {
    if (!stream) return null;
    const mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
    mediaRecorderRef.current = mediaRecorder;
    
    const chunks = [];
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunks.push(e.data);
    };
    
    return new Promise((resolve) => {
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'video/webm' });
        resolve(blob);
      };
      mediaRecorder.start();
      setIsRecording(true);
    });
  }, [stream]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, []);

  const cleanupStream = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
  }, [stream]);

  return { permissionState, requestPermissions, startRecording, stopRecording, cleanupStream, isRecording, stream };
}
