import { useMemo, useState } from "react";

export function useAdminFilters(candidates, pageSize = 10) {
  const [filters, setFilters] = useState({
    district: "all",
    language: "all",
    fitment: "all",
  });
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });
  const [currentPage, setCurrentPage] = useState(1);

  const filteredAndSortedCandidates = useMemo(() => {
    let result = candidates.filter((candidate) => {
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

    if (sortConfig.key) {
      result.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === "asc" ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === "asc" ? 1 : -1;
        }
        return 0;
      });
    }

    return result;
  }, [candidates, filters, sortConfig]);

  const totalPages = Math.max(1, Math.ceil(filteredAndSortedCandidates.length / pageSize));
  const safePage = Math.min(currentPage, totalPages);

  const paginatedCandidates = useMemo(() => {
    const startIndex = (safePage - 1) * pageSize;
    return filteredAndSortedCandidates.slice(startIndex, startIndex + pageSize);
  }, [filteredAndSortedCandidates, safePage, pageSize]);

  const handleSort = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }
    setSortConfig({ key, direction });
  };

  return {
    filters,
    setFilters,
    sortConfig,
    handleSort,
    currentPage: safePage,
    setCurrentPage,
    totalPages,
    paginatedCandidates,
  };
}
