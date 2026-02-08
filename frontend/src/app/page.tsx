"use client";
import { useMemo, useState, useEffect, useCallback } from "react";

import dynamic from "next/dynamic";
import { SectionCards } from "@/src/components/section-cards";
import { InputInline } from "@/src/components/search";
import { HeroSection } from "../components/hero-section";
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
const ChartLineInteractive = dynamic(
  () =>
    import("@/src/components/chart-line-interactive").then(
      (mod) => mod.ChartLineInteractive,
    ),
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
const ChartPieLegend = dynamic(
  () =>
    import("../components/chart-pie-legend").then((mod) => mod.ChartPieLegend),
  { ssr: false },
);

export default function HomePage() {
  const [tableData, setTableData] = useState<any[]>([]);
  const [stats, setStats] = useState<any>({
    total: 0,
    positive: 0,
    negative: 0,
    neutral: 0,
  });
  const [chartData, setChartData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const searchParams = useSearchParams();
  const keyword = searchParams.get("keyword") || "";

  const loadDashboardData = useCallback(async () => {
    setLoading(true);
    try {
      const query = keyword ? `?keyword=${encodeURIComponent(keyword)}` : "";

      const [statsRes, chartRes, tableRes] = await Promise.all([
        fetch(`http://127.0.0.1:8000/api/sentiment/stats${query}`, {
          cache: "no-store",
        }),
        fetch(`http://127.0.0.1:8000/api/sentiment/chart${query}`, {
          cache: "no-store",
        }),
        fetch(
          `http://127.0.0.1:8000/api/sentiment/list${query}&page_size=200`,
          { cache: "no-store" },
        ),
      ]);

      const [statsJson, chartJson, tableJson] = await Promise.all([
        statsRes.json(),
        chartRes.json(),
        tableRes.json(),
      ]);

      setStats(statsJson);
      setChartData(chartJson);
      setTableData(Array.isArray(tableJson) ? tableJson : tableJson.data || []);
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
  const summary = useMemo(() => { // This was removed as sentimentSummary is sufficient
    if (stats.total === 0) return "Menunggu data...";
    const posPercent = ((stats.positive / stats.total) * 100).toFixed(1);
    const negPercent = ((stats.negative / stats.total) * 100).toFixed(1);
    return stats.positive > stats.negative
      ? `Dominan positif (${posPercent}%)`
      : `Dominan negatif (${negPercent}%)`;
  }, [stats]);

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
  // const platform = { // This was removed as platformDistribution is now used
  //   News: rawData.filter(
  //     (item: any) =>
  //       item.platform && item.platform.toString().toLowerCase() === "news",
  //   ).length,
  //   Twitter: rawData.filter(
  //     (item: any) =>
  //       item.platform && item.platform.toString().toLowerCase() === "twitter",
  //   ).length,
  //   Tiktok: rawData.filter(
  //     (item: any) =>
  //       item.platform && item.platform.toString().toLowerCase() === "tiktok",
  //   ).length,
  //   Youtube: rawData.filter(
  //     (item: any) =>
  //       item.platform && item.platform.toString().toLowerCase() === "youtube",
  //   ).length,
  // };

  const platformDistribution = useMemo(() => {
    const platforms = ["News", "Twitter", "Tiktok", "Youtube"];
    return platforms.map((p) => ({
      label: p.charAt(0).toUpperCase() + p.slice(1),
      value: tableData.filter((i) => i.platform?.toLowerCase() === p).length,
      fill: `var(--color-${p})`,
    }));
  }, [tableData]);

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
          <ChartAreaInteractive data={chartData} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        <div className="md:col-span-8">
          <WordCloudCard data={wordCloudData} />
        </div>
        <div className="md:col-span-4">
          <ChartPieDonut
            title="Distribution platform"
            description="Distribusi Platform"
            chartData={platformDistribution}
          />
        </div>
      </div>

      <div className="flex flex-col gap-6">
        <DataTable data={tableData} />
        <div className="w-full">
          <ChartLineInteractive />
        </div>
      </div>
    </div>
  );
}
