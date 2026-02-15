import { useQuery } from "@tanstack/react-query";

const API_BASE_URL = "http://127.0.0.1:8000";

// Fetcher functions
const fetchStats = async (query: string) => {
  const res = await fetch(`${API_BASE_URL}/api/sentiment/stats${query}`);
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
};

const fetchCharts = async (query: string) => {
  const res = await fetch(`${API_BASE_URL}/api/sentiment/chart${query}`);
  if (!res.ok) throw new Error("Failed to fetch charts");
  return res.json();
};

const fetchPlatformStats = async (query: string) => {
  const res = await fetch(`${API_BASE_URL}/api/sentiment/platform-stats${query}`);
  if (!res.ok) throw new Error("Failed to fetch platform stats");
  return res.json();
};

const fetchWordCloud = async (query: string) => {
  const res = await fetch(`${API_BASE_URL}/api/sentiment/wordcloud${query}`);
  if (!res.ok) throw new Error("Failed to fetch word cloud");
  return res.json();
};

const fetchTableData = async (query: string) => {
  const res = await fetch(
    `${API_BASE_URL}/api/sentiment/list${query}${query ? "&" : "?"}page_size=200`
  );
  if (!res.ok) throw new Error("Failed to fetch table data");
  return res.json();
};

export function useDashboardData(keyword: string) {
  const query = keyword ? `?keyword=${encodeURIComponent(keyword)}` : "";

  const statsQuery = useQuery({
    queryKey: ["stats", keyword],
    queryFn: () => fetchStats(query),
    staleTime: 60 * 1000, 
    placeholderData: (previousData) => previousData,
  });

  const chartQuery = useQuery({
    queryKey: ["chart", keyword],
    queryFn: () => fetchCharts(query),
    staleTime: 60 * 1000,
    placeholderData: (previousData) => previousData,
  });

  const platformQuery = useQuery({
    queryKey: ["platform-stats", keyword],
    queryFn: () => fetchPlatformStats(query),
    staleTime: 60 * 1000,
    placeholderData: (previousData) => previousData,
  });

  const wordCloudQuery = useQuery({
    queryKey: ["wordcloud", keyword],
    queryFn: () => fetchWordCloud(query),
    staleTime: 60 * 1000,
    placeholderData: (previousData) => previousData,
  });

  const tableQuery = useQuery({
    queryKey: ["table-data", keyword],
    queryFn: () => fetchTableData(query),
    staleTime: 60 * 1000,
    placeholderData: (previousData) => previousData,
  });

  // Derived loading state - only true on INITIAL load
  const isLoading =
    statsQuery.isPending && !statsQuery.data &&
    chartQuery.isPending && !chartQuery.data &&
    platformQuery.isPending && !platformQuery.data &&
    wordCloudQuery.isPending && !wordCloudQuery.data;

  return {
    stats: statsQuery.data || { total: 0, positive: 0, negative: 0, neutral: 0 },
    chartData: chartQuery.data || [],
    platformData: platformQuery.data || [],
    wordCloudData: wordCloudQuery.data || [],
    tableData: Array.isArray(tableQuery.data) ? tableQuery.data : tableQuery.data?.data || [],
    isLoading,
    isRefetching:
      statsQuery.isRefetching ||
      chartQuery.isRefetching ||
      platformQuery.isRefetching ||
      wordCloudQuery.isRefetching ||
      tableQuery.isRefetching,
  };
}
