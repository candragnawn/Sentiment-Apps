"use client";
import { useMemo, useState, useEffect, useCallback } from "react";
import dynamic from "next/dynamic";
import { SectionCards } from "@/src/components/section-cards";
import { useSearchParams } from "next/navigation";

const ChartAreaInteractive = dynamic(
  () =>
    import("@/src/components/chart-area-interactive").then(
      (mod) => mod.ChartAreaInteractive,
    ),
  { ssr: false },
);
const DataTable = dynamic(
  () => import("@/src/components/data-table").then((mod) => mod.DataTable),
  { ssr: false },
);
const ChartPieDonut = dynamic(
  () =>
    import("@/src/components/chart-pie-donut").then((mod) => mod.ChartPieDonut),
  { ssr: false }, 
);
const WordCloudCard = dynamic(
  () => import("@/src/components/world-cloud").then((mod) => mod.WordCloudCard),
  { ssr: false },
);

export default function DashboardPage() {
  const [tableData, setTableData] = useState<any[]>([]);
  const [stats, setStats] = useState<any>({
    total: 0,
    positive: 0,
    negative: 0,
    neutral: 0,
  });
  const [chartData, setChartData] = useState<any[]>([]);
  const [platformData, setPlatformData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const searchParams = useSearchParams();
  const keyword = searchParams.get("keyword") || "";

  const loadDashboardData = useCallback(async () => {
    setLoading(true);
    try {
      const query = keyword ? `?keyword=${encodeURIComponent(keyword)}` : "";

      const [statsRes, chartRes, tableRes, platformRes] = await Promise.all([
        fetch(`http://127.0.0.1:8000/api/sentiment/stats${query}`, {
          cache: "no-store",
        }),
        fetch(`http://127.0.0.1:8000/api/sentiment/chart${query}`, {
          cache: "no-store",
        }),
        fetch(`http://127.0.0.1:8000/api/sentiment/list${query}${query ? '&' : '?'}page_size=500`, {
          cache: "no-store",
        }),
        fetch(`http://127.0.0.1:8000/api/sentiment/platform-stats${query}`, {
          cache: "no-store",
        }),
      ]);

      const [statsJson, chartJson, tableJson, platformJson] = await Promise.all([
        statsRes.json(),
        chartRes.json(),
        tableRes.json(),
        platformRes.json(),
      ]);

      setStats(statsJson);
      setChartData(chartJson);
      setTableData(Array.isArray(tableJson) ? tableJson : tableJson.data || []);
      setPlatformData(platformJson);
    } catch (error) {
      console.error("Failed to load dashboard data", error);
    } finally {
      setLoading(false);
    }
  }, [keyword]);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  const positivePercent =
    stats.total > 0 ? ((stats.positive / stats.total) * 100).toFixed(1) : 0;
  const negativePercent =
    stats.total > 0 ? ((stats.negative / stats.total) * 100).toFixed(1) : 0;

  const sentimentSummary =
    stats.positive > stats.negative
      ? `Dominan sentimen positif (${positivePercent}%)`
      : `Dominan sentimen negatif (${negativePercent}%)`;

  const sentimentData = useMemo(
    () => [
      {
        label: "positive",
        value: stats.positive,
        fill: "var(--color-positive)",
      },
      {
        label: "negative",
        value: stats.negative,
        fill: "var(--color-negative)",
      },
      { label: "neutral", value: stats.neutral, fill: "var(--color-neutral)" },
    ],
    [stats],
  );

  const platformDistribution = useMemo(() => {
    if (platformData && platformData.length > 0) {
      return platformData.map(item => ({
        ...item,
        label: item.label.toLowerCase()
      }));
    }
    const platforms = ["news", "twitter", "tiktok", "youtube"];
    return platforms.map((p) => ({
      label: p,
      value: tableData.filter((i) => i.platform?.toLowerCase().trim() === p).length,
      fill: `var(--color-${p})`,
    }));
  }, [platformData, tableData]);

  const wordCloudData = useMemo(() => {
    const wordMap = new Map<string, number>();
    tableData.forEach((item) => {
      item.top_keyword?.forEach((word: string) => {
        wordMap.set(word, (wordMap.get(word) || 0) + 1);
      });
    });

    return Array.from(wordMap.entries())
      .map(([text, value]) => ({ text, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 350);
  }, [tableData]);

  return (
    <div className="flex flex-1 flex-col gap-6 p-4 md:p-6 pt-0">
      <div className="flex flex-col gap-2">
        <h1 className="text-xl font-bold tracking-tight">
          Sentimen dari <span className="text-primary">{keyword}</span>
        </h1>
        <p className="text-muted-foreground">
          Ringkasan analisis sentimen lintas {keyword}platform secara real-time.
        </p>
      </div>

      <div className="w-full">
        <div className="@container/main">
          <SectionCards
            total={stats.total}
            positive={stats.positive}
            negative={stats.negative}
            neutral={stats.neutral}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        <div className="md:col-span-4">
          <ChartPieDonut
            title="Distribution Label"
            description="Distribusi Sentiment hari ini"
            footer={sentimentSummary}
            chartData={sentimentData}
          />
        </div>

        <div className="md:col-span-8">
          <WordCloudCard data={wordCloudData} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        <div className="md:col-span-8">
          <ChartAreaInteractive data={chartData} />
        </div>
        <div className="md:col-span-4">
          <ChartPieDonut
            title="Distribution platform"
            description="Distribusi Platform"
            chartData={platformDistribution}
          />
        </div>
      </div>
    </div>
  );
}
