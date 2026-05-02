function IntegrityFlag({ flags = [] }) {
  if (!flags.length) {
    return <span className="status-pill status-good">No active flags</span>;
  }

  return (
    <div className="flag-list">
      {flags.map((flag) => (
        <span key={flag} className="status-pill status-alert">
          {flag}
        </span>
      ))}
    </div>
  );
}

export default IntegrityFlag;
