function FitmentBadge({ label }) {
  return <span className={`badge badge-${label?.toLowerCase()}`}>{label || "Pending"}</span>;
}

export default FitmentBadge;
