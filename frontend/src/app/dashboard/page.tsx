"use client";
import { useMemo, Suspense } from "react";
import dynamic from "next/dynamic";
import { SectionCards } from "@/src/components/section-cards";
import { useSearchParams } from "next/navigation";
import { useDashboardData } from "@/src/hooks/use-dashboard-data"; // Import the hook

const ChartAreaInteractive = dynamic(
  () =>
    import("@/src/components/chart-area-interactive").then(
      (mod) => mod.ChartAreaInteractive,
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

// Helper function safely exported
function DashboardContent() {
  const searchParams = useSearchParams();
  const keyword = searchParams.get("keyword") || "";
  
  const { stats, chartData, platformData, tableData, isLoading } = useDashboardData(keyword);
  
  const platformDistribution = useMemo(() => {
    if (platformData && platformData.length > 0) {
      return platformData.map((item: any) => ({
        ...item,
        label: item.label.toLowerCase()
      }));
    }
    const platforms = ["news", "twitter", "tiktok", "youtube"];
    return platforms.map((p) => ({
      label: p,
      value: tableData.filter((i: any) => i.platform?.toLowerCase().trim() === p).length,
      fill: `var(--color-${p})`,
    }));
  }, [platformData, tableData]);

  const wordCloudData = useMemo(() => {
    const wordMap = new Map<string, number>();
    tableData.forEach((item: any) => {
      item.top_keyword?.forEach((word: string) => {
        wordMap.set(word, (wordMap.get(word) || 0) + 1);
      });
    });

    return Array.from(wordMap.entries())
      .map(([text, value]) => ({ text, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 50);
  }, [tableData]);

  const positivePercent =
    stats.total > 0 ? ((stats.positive / stats.total) * 100).toFixed(1) : "0";
  const negativePercent =
    stats.total > 0 ? ((stats.negative / stats.total) * 100).toFixed(1) : "0";

  const sentimentSummary =
    stats.positive > stats.negative
      ? `Dominan sentimen positif (${positivePercent}%)`
      : `Dominan sentimen negatif (${negativePercent}%)`;

  const sentimentData = [
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
  ];

  if (isLoading && !stats.total) {
     return (
      <div className="flex flex-1 items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="flex flex-1 flex-col gap-6 p-4 md:p-6 pt-0">
      <div className="flex flex-col gap-2">
        <h1 className="text-xl font-medium tracking-tight">
          {keyword ? (
            <>
              Analisis Sentimen dari{" "}
              <span className="text-primary font-bold">{keyword}</span>
            </>
          ) : (
            "Analisis Sentimen Terkini"
          )}
        </h1>
        <p className="text-muted-foreground">
          Ringkasan analisis sentimen lintas platform secara real-time
          {keyword ? ` untuk "${keyword}"` : "."}
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

export default function DashboardPage() {
  return (
    <Suspense fallback={
      <div className="flex flex-1 items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    }>
      <DashboardContent />
    </Suspense>
  );
}
