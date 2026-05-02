import { Navigate, Route, Routes } from "react-router-dom";
import CandidateDetail from "../pages/admin/CandidateDetail";
import Dashboard from "../pages/admin/Dashboard";
import Login from "../pages/admin/Login";
import { useAdminContext } from "../context/AdminContext";

function AdminRoutes() {
  const { isAuthenticated } = useAdminContext();

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={isAuthenticated ? <Dashboard /> : <Navigate to="/admin/login" replace />} />
      <Route
        path="/candidates/:candidateId"
        element={isAuthenticated ? <CandidateDetail /> : <Navigate to="/admin/login" replace />}
      />
      <Route path="*" element={<Navigate to={isAuthenticated ? "/admin" : "/admin/login"} replace />} />
    </Routes>
  );
}

export default AdminRoutes;
