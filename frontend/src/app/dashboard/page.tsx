"use client";

import { useEffect, useState } from "react";
import { ChartAreaInteractive } from "./components/chart-area-interactive";
import { DataTable } from "./components/data-table";
import { SectionCards } from "@/src/app/dashboard/components/section-cards";
import { InputInline } from "@/src/app/dashboard/components/search";

export default function DashboardPage() {
  const [rawData, setRawData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/api/sentiment/list");
      const json = await response.json();
      setRawData(Array.isArray(json) ? json : json.data || []);
    } catch (error) {
      console.error("Failed to load data", error);
    } finally {
      setLoading(false);
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
    <div className="@container/main flex flex-1 flex-col gap-2">
      <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
        <div className="px-5 lg:px-6">
          <InputInline />

          <SectionCards
            total={stats.total}
            positive={stats.positive}
            negative={stats.negative}
            neutral={stats.neutral}
          />

          <div className="mt-6">
            <ChartAreaInteractive data={rawData} />
          </div>

          <div className="mt-6">
            <DataTable data={rawData} />
          </div>
        </div>
      </div>
    </div>
  );
}
