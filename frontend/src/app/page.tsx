"use client";

import { useState, useEffect } from "react";
import { SectionCards } from "@/src/components/section-cards";
import { ChartAreaInteractive } from "@/src//components/chart-area-interactive";
import { DataTable } from "@/src//components/data-table";
import { ChartLineInteractive } from "@/src//components/chart-line-interactive";
import { ChartPieDonut } from "@/src//components/chart-pie-donut";
import { WordCloudCard } from "@/src/components/world-cloud";

export default function HomePage() {
  const [rawData, setRawData] = useState<any[]>([]);

  const loadData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/sentiment/list");
      const json = await response.json();
      setRawData(Array.isArray(json) ? json : json.data || []);
    } catch (error) {
      console.error("Failed to load data", error);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const stats = {
    total: rawData.length,
    positive: rawData.filter((item: any) => item.label === "positive").length,
    negative: rawData.filter((item: any) => item.label === "negative").length,
    neutral: rawData.filter((item: any) => item.label === "neutral").length,
  };

  const positivePercent =
    stats.total > 0 ? ((stats.positive / stats.total) * 100).toFixed(1) : 0;
  const negativePercent =
    stats.total > 0 ? ((stats.negative / stats.total) * 100).toFixed(1) : 0;

  const sentimentSummary =
    stats.positive > stats.negative
      ? `Dominan sentimen positif (${positivePercent}%)`
      : `Dominan sentimen negatif (${negativePercent}%)`;

  const SentimentDistribution = [
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
  const PlatformDistribution = [
    { label: "News", value: platform.News, fill: "var(--color-news)" },
    { label: "Twitter", value: platform.Twitter, fill: "var(--color-twitter)" },
    { label: "Tiktok", value: platform.Tiktok, fill: "var(--color-tiktok)" },
    { label: "Youtube", value: platform.Youtube, fill: "var(--color-youtube)" },
  ];
  const wordCloudData = rawData.reduce((acc: any[], item: any) => {
    item.top_keyword?.forEach((word: string) => {
      const existing = acc.find((w) => w.text === word);
      if (existing) {
        existing.value += 1;
      } else {
        acc.push({ text: word, value: 1 });
      }
    });
    return acc;
  }, []);

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
            chartData={SentimentDistribution}
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
          <ChartPieDonut
            title="Distribution platform"
            description="Distribusi Platform"
            chartData={PlatformDistribution}
          />
        </div>
      </div>

      <div className="flex flex-col gap-6">
        <DataTable data={rawData} />
        <div className="w-full">
          <ChartLineInteractive data={rawData} />
        </div>
        <div className="  "></div>
      </div>
    </div>
  );
}
