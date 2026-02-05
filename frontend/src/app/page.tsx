"use client";
import { useMemo, useState, useEffect, useCallback } from "react";

import dynamic from "next/dynamic";
import { SectionCards } from "@/src/components/section-cards";
import { InputInline } from "@/src/components/search";

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
  const [rawData, setRawData] = useState<any[]>([]);

  const loadData = useCallback(async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/sentiment/list", {
        cache: "no-store",
      });
      const json = await response.json();
      setRawData(Array.isArray(json) ? json : json.data || []);
    } catch (error) {
      console.error("Failed to load data", error);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, []);

  const stats = useMemo(
    () => ({
      total: rawData.length,
      positive: rawData.filter((item: any) => item.label === "positive").length,
      negative: rawData.filter((item: any) => item.label === "negative").length,
      neutral: rawData.filter((item: any) => item.label === "neutral").length,
    }),
    [rawData],
  );

  const positivePercent =
    stats.total > 0 ? ((stats.positive / stats.total) * 100).toFixed(1) : 0;
  const negativePercent =
    stats.total > 0 ? ((stats.negative / stats.total) * 100).toFixed(1) : 0;

  const sentimentSummary =
    stats.positive > stats.negative
      ? `Dominan sentimen positif (${positivePercent}%)`
      : `Dominan sentimen negatif (${negativePercent}%)`;
  const summary = useMemo(() => {
    if (stats.total === 0) return "Menunggu data...";
    const posPercent = ((stats.positive / stats.total) * 100).toFixed(1);
    const negPercent = ((stats.negative / stats.total) * 100).toFixed(1);
    return stats.positive > stats.negative
      ? `Dominan positif (${posPercent}%)`
      : `Dominan negatif (${negPercent}%)`;
  }, [stats]);

  const sentimentData = [
    { label: "positive", value: stats.positive, fill: "var(--color-positive)" },
    { label: "negative", value: stats.negative, fill: "var(--color-negative)" },
    { label: "neutral", value: stats.neutral, fill: "var(--color-neutral)" },
  ];
  const platform = {
    News: rawData.filter(
      (item: any) =>
        item.platform && item.platform.toString().toLowerCase() === "news",
    ).length,
    Twitter: rawData.filter(
      (item: any) =>
        item.platform && item.platform.toString().toLowerCase() === "twitter",
    ).length,
    Tiktok: rawData.filter(
      (item: any) =>
        item.platform && item.platform.toString().toLowerCase() === "tiktok",
    ).length,
    Youtube: rawData.filter(
      (item: any) =>
        item.platform && item.platform.toString().toLowerCase() === "youtube",
    ).length,
  };

  const platformDistribution = useMemo(() => {
    const platforms = ["news", "twitter", "tiktok", "youtube"];
    return platforms.map((p) => ({
      label: p.charAt(0).toUpperCase() + p.slice(1),
      value: rawData.filter((i) => i.platform?.toLowerCase() === p).length,
      fill: `var(--color-${p})`,
    }));
  }, [rawData]);

  const wordCloudData = useMemo(() => {
    const acc: any[] = [];
    rawData.forEach((item) => {
      item.top_keyword?.forEach((word: string) => {
        const existing = acc.find((w) => w.text === word);
        if (existing) existing.value += 1;
        else acc.push({ text: word, value: 1 });
      });
    });
    return acc.sort((a, b) => b.value - a.value).slice(0, 50); // Batasi 50 kata biar gak berat
  }, [rawData]);

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
          <ChartAreaInteractive data={rawData} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        <div className="md:col-span-8">
          {" "}
          <WordCloudCard data={wordCloudData} />
        </div>
        <div className="md:col-span-4">
          <ChartPieLegend
            title="Distribution platform"
            description="Distribusi Platform"
            chartData={platform}
          />
        </div>
        f
      </div>

      <div className="flex flex-col gap-6">
        <DataTable data={rawData} />
        <div className="w-full">
          <ChartLineInteractive />
        </div>
        <div className="  "></div>
      </div>
    </div>
  );
}
