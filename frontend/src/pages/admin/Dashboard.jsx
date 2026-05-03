import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Filters from "../../components/Filters";
import FitmentBadge from "../../components/FitmentBadge";
import ScoreCard from "../../components/ScoreCard";
import { useAdminContext } from "../../context/AdminContext";
import { useAdminFilters } from "../../hooks/useAdminFilters";
import { getAdminStats, getCandidates, updateCandidateStatus } from "../../services/admin.service";

function Dashboard() {
  const { logout } = useAdminContext();
  const [stats, setStats] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const {
    filters,
    setFilters,
    sortConfig,
    handleSort,
    currentPage,
    setCurrentPage,
    totalPages,
    paginatedCandidates,
  } = useAdminFilters(candidates);

  useEffect(() => {
    async function loadData() {
      const [statsResponse, candidatesResponse] = await Promise.all([getAdminStats(), getCandidates()]);
      setStats(statsResponse);
      setCandidates(candidatesResponse.items);
    }

    loadData();
  }, []);

  const districts = Array.from(new Set(candidates.map((candidate) => candidate.district))).sort();

  async function handleShortlist(candidateId, currentlyShortlisted) {
    const action = currentlyShortlisted ? "flag_review" : "shortlist_job";
    const updated = await updateCandidateStatus(candidateId, action);
    setCandidates((current) => current.map((candidate) => (candidate.id === candidateId ? updated : candidate)));
  }

  return (
    <main className="screen">
      <section className="panel">
        <div className="heading-row">
          <div>
            <p className="eyebrow">Admin Dashboard</p>
            <h1>Candidate review workspace</h1>
          </div>
          <button type="button" className="button button-secondary" onClick={logout}>
            Log Out
          </button>
        </div>

        {stats ? (
          <div className="metrics-grid">
            <ScoreCard title="Total candidates" value={stats.total_candidates} description="All recorded sessions" />
            <ScoreCard title="Shortlisted" value={stats.shortlisted_candidates} description="Marked for next step" />
            <ScoreCard title="Pending review" value={stats.pending_review} description="Officer action needed" />
            <ScoreCard title="Job ready" value={stats.job_ready} description="High-confidence candidates" />
          </div>
        ) : null}

        <Filters
          districts={districts}
          filters={filters}
          onChange={(field, value) => setFilters((current) => ({ ...current, [field]: value }))}
        />

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th onClick={() => handleSort("full_name")} style={{ cursor: "pointer", userSelect: "none" }}>
                  Name {sortConfig.key === "full_name" ? (sortConfig.direction === "asc" ? "↑" : "↓") : ""}
                </th>
                <th onClick={() => handleSort("district")} style={{ cursor: "pointer", userSelect: "none" }}>
                  District {sortConfig.key === "district" ? (sortConfig.direction === "asc" ? "↑" : "↓") : ""}
                </th>
                <th onClick={() => handleSort("role_applied")} style={{ cursor: "pointer", userSelect: "none" }}>
                  Role {sortConfig.key === "role_applied" ? (sortConfig.direction === "asc" ? "↑" : "↓") : ""}
                </th>
                <th onClick={() => handleSort("language")} style={{ cursor: "pointer", userSelect: "none" }}>
                  Language {sortConfig.key === "language" ? (sortConfig.direction === "asc" ? "↑" : "↓") : ""}
                </th>
                <th onClick={() => handleSort("fitment_label")} style={{ cursor: "pointer", userSelect: "none" }}>
                  Fitment {sortConfig.key === "fitment_label" ? (sortConfig.direction === "asc" ? "↑" : "↓") : ""}
                </th>
                <th onClick={() => handleSort("overall_score")} style={{ cursor: "pointer", userSelect: "none" }}>
                  Score {sortConfig.key === "overall_score" ? (sortConfig.direction === "asc" ? "↑" : "↓") : ""}
                </th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {paginatedCandidates.map((candidate) => (
                <tr key={candidate.id}>
                  <td>
                    <Link to={`/admin/candidates/${candidate.id}`}>{candidate.full_name}</Link>
                  </td>
                  <td>{candidate.district}</td>
                  <td>{candidate.role_applied}</td>
                  <td>{candidate.language}</td>
                  <td>
                    <FitmentBadge label={candidate.fitment_label} />
                  </td>
                  <td>{candidate.overall_score.toFixed(2)}</td>
                  <td>
                    <button
                      type="button"
                      className="button button-inline"
                      onClick={() => handleShortlist(candidate.id, candidate.shortlisted)}
                    >
                      {candidate.shortlisted ? "Unshortlist" : "Shortlist"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {totalPages > 1 && (
          <div className="pagination-controls" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "16px" }}>
            <button 
              type="button" 
              className="button button-secondary" 
              onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              disabled={currentPage === 1}
            >
              Previous
            </button>
            <span>Page {currentPage} of {totalPages}</span>
            <button 
              type="button" 
              className="button button-secondary" 
              onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
              disabled={currentPage === totalPages}
            >
              Next
            </button>
          </div>
        )}
      </section>
    </main>
  );
}

export default Dashboard;
