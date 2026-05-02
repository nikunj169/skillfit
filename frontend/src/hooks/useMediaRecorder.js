import { useState } from "react";

export function useMediaRecorder() {
  const [permissionState, setPermissionState] = useState("idle");

  async function requestPermissions() {
    try {
      if (navigator.mediaDevices?.getUserMedia) {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        stream.getTracks().forEach((track) => track.stop());
      }
      setPermissionState("granted");
      return true;
    } catch {
      setPermissionState("denied");
      return false;
    }
  }

  return { permissionState, requestPermissions };
}
