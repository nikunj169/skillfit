import { Navigate, Route, Routes } from "react-router-dom";
import Interview from "../pages/candidate/Interview";
import InterviewComplete from "../pages/candidate/InterviewComplete";
import Landing from "../pages/candidate/Landing";
import PermissionGate from "../pages/candidate/PermissionGate";
import Processing from "../pages/candidate/Processing";
import Registration from "../pages/candidate/Registration";

function CandidateRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/register" element={<Registration />} />
      <Route path="/permissions" element={<PermissionGate />} />
      <Route path="/interview" element={<Interview />} />
      <Route path="/processing" element={<Processing />} />
      <Route path="/complete" element={<InterviewComplete />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default CandidateRoutes;
