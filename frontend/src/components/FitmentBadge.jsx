function FitmentBadge({ label, displayLabel }) {
  return (
    <span className={`badge badge-${label?.toLowerCase()}`}>
      {displayLabel ?? label ?? "Pending"}
    </span>
  );
}

export default FitmentBadge;
