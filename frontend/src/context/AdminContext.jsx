import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { setAdminToken } from "../services/api";

const AdminContext = createContext(null);
const ADMIN_TOKEN_KEY = "skillfit_admin_token";

export function useAdminContext() {
  const context = useContext(AdminContext);
  if (!context) {
    throw new Error("useAdminContext must be used within AdminContextProvider.");
  }
  return context;
}

function AdminContextProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(ADMIN_TOKEN_KEY) || "");

  useEffect(() => {
    setAdminToken(token);
    if (token) {
      localStorage.setItem(ADMIN_TOKEN_KEY, token);
    } else {
      localStorage.removeItem(ADMIN_TOKEN_KEY);
    }
  }, [token]);

  const value = useMemo(
    () => ({
      token,
      isAuthenticated: Boolean(token),
      login(nextToken) {
        setToken(nextToken);
      },
      logout() {
        setToken("");
      },
    }),
    [token]
  );

  return <AdminContext.Provider value={value}>{children}</AdminContext.Provider>;
}

export default AdminContextProvider;
