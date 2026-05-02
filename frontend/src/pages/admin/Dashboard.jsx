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
  const { filters, setFilters, filteredCandidates } = useAdminFilters(candidates);

  useEffect(() => {
    async function loadData() {
      const [statsResponse, candidatesResponse] = await Promise.all([getAdminStats(), getCandidates()]);
      setStats(statsResponse);
      setCandidates(candidatesResponse.items);
    }

    loadData();
  }, []);

  const districts = Array.from(new Set(candidates.map((candidate) => candidate.district))).sort();

  async function handleShortlist(candidateId, shortlisted) {
    const updated = await updateCandidateStatus(candidateId, shortlisted);
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
                <th>Name</th>
                <th>District</th>
                <th>Role</th>
                <th>Language</th>
                <th>Fitment</th>
                <th>Score</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredCandidates.map((candidate) => (
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
                      onClick={() => handleShortlist(candidate.id, !candidate.shortlisted)}
                    >
                      {candidate.shortlisted ? "Unshortlist" : "Shortlist"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}

export default Dashboard;
