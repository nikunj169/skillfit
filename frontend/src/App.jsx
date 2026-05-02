import { Navigate, Route, Routes } from "react-router-dom";
import AdminContextProvider from "./context/AdminContext";
import SessionContextProvider from "./context/SessionContext";
import AdminRoutes from "./routes/AdminRoutes";
import CandidateRoutes from "./routes/CandidateRoutes";

function App() {
  return (
    <AdminContextProvider>
      <SessionContextProvider>
        <Routes>
          <Route path="/admin/*" element={<AdminRoutes />} />
          <Route path="/*" element={<CandidateRoutes />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </SessionContextProvider>
    </AdminContextProvider>
  );
}

export default App;
