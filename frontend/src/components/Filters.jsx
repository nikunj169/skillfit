function Filters({ districts, filters, onChange }) {
  return (
    <div className="filter-grid">
      <label className="form-field">
        <span>District</span>
        <select value={filters.district} onChange={(event) => onChange("district", event.target.value)}>
          <option value="all">All districts</option>
          {districts.map((district) => (
            <option key={district} value={district}>
              {district}
            </option>
          ))}
        </select>
      </label>

      <label className="form-field">
        <span>Language</span>
        <select value={filters.language} onChange={(event) => onChange("language", event.target.value)}>
          <option value="all">All languages</option>
          <option value="en">English</option>
          <option value="hi">Hindi</option>
          <option value="kn">Kannada</option>
        </select>
      </label>

      <label className="form-field">
        <span>Fitment</span>
        <select value={filters.fitment} onChange={(event) => onChange("fitment", event.target.value)}>
          <option value="all">All statuses</option>
          <option value="JOB_READY">Job Ready</option>
          <option value="REQUIRES_UPSKILLING">Requires Upskilling</option>
          <option value="REQUIRES_MANUAL_VERIFICATION">Manual Review</option>
          <option value="LOW_QUALITY_SUBMISSION">Low Quality</option>
          <option value="SUSPECTED_DUPLICATE">Suspected Duplicate</option>
        </select>
      </label>
    </div>
  );
}

export default Filters;
