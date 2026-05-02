import { createContext, useContext, useMemo, useState } from "react";

const SessionContext = createContext(null);

export function useSessionContext() {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error("useSessionContext must be used within SessionContextProvider.");
  }
  return context;
}

function SessionContextProvider({ children }) {
  const [registration, setRegistration] = useState({
    full_name: "",
    district: "",
    role_applied: "Electrician",
    language: "en",
    phone_number: "",
  });
  const [session, setSession] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [result, setResult] = useState(null);

  const value = useMemo(
    () => ({
      registration,
      setRegistration,
      session,
      setSession,
      questions,
      setQuestions,
      result,
      setResult,
      resetSession() {
        setSession(null);
        setQuestions([]);
        setResult(null);
      },
    }),
    [questions, registration, result, session]
  );

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

export default SessionContextProvider;
