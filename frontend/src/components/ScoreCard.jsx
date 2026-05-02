import { formatScore } from "../utils/formatters";

function ScoreCard({ title, value, description }) {
  return (
    <article className="metric-card">
      <p className="metric-label">{title}</p>
      <strong className="metric-value">{formatScore(value)}</strong>
      <p className="metric-description">{description}</p>
    </article>
  );
}

export default ScoreCard;
