"use client";

import { useState, useEffect } from "react";
import { SectionCards } from "@/src/app/dashboard/components/section-cards";
import { ChartAreaInteractive } from "@/src/app/dashboard/components/chart-area-interactive";

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

  return (
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      <div className="@container/main flex flex-1 flex-col gap-4">
        <SectionCards
          total={stats.total}
          positive={stats.positive}
          negative={stats.negative}
          neutral={stats.neutral}
        />
        <div className="min-h-[100vh] flex-1 rounded-xl md:min-h-min">
          <ChartAreaInteractive data={rawData} />
        </div>
      </div>
    </div>
  );
}
