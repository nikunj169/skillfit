import { useMemo, useState } from "react";

export function useAdminFilters(candidates) {
  const [filters, setFilters] = useState({
    district: "all",
    language: "all",
    fitment: "all",
  });

  const filteredCandidates = useMemo(() => {
    return candidates.filter((candidate) => {
      if (filters.district !== "all" && candidate.district !== filters.district) {
        return false;
      }
      if (filters.language !== "all" && candidate.language !== filters.language) {
        return false;
      }
      if (filters.fitment !== "all" && candidate.fitment_label !== filters.fitment) {
        return false;
      }
      return true;
    });
  }, [candidates, filters]);

  return { filters, setFilters, filteredCandidates };
}
