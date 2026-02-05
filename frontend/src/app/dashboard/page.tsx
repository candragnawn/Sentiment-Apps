"use client";

import { useEffect, useState } from "react";
import { ChartAreaInteractive } from "@/src/components/chart-area-interactive";
import { DataTable } from "@/src/components/data-table";
import { SectionCards } from "@/src/components/section-cards";
import { InputInline } from "@/src/components/search";
import { HeroSection } from "@/src/components/hero-section";
import { Toaster, toast } from "sonner";

export default function DashboardPage() {
  const [rawData, setRawData] = useState<any[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [latestResult, setLatestResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/sentiment/list");
      const json = await response.json();
      const cleanedData = Array.isArray(json) ? json : json.data || [];
      setRawData(cleanedData);
      if (cleanedData.length > 0) {
        setLatestResult(cleanedData[0]);
      }
    } catch (error) {
      console.error("Failed to load data", error);
    } finally {
    }
  };
  useEffect(() => {
    loadData();
    const interval = setInterval(() => {
      loadData();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const stats = {
    total: rawData.length,
    positive: rawData.filter((item: any) => item.label === "positive").length,
    negative: rawData.filter((item: any) => item.label === "negative").length,
    neutral: rawData.filter((item: any) => item.label === "neutral").length,
  };

  const handleAnalyzeComplete = async () => {
    await loadData();
    setIsAnalyzing(false);
    toast.success("analisis complete", {
      description: "new data has been analyzed successfully",
    });
  };

  const handleAnalyzeStart = () => {
    setIsAnalyzing(true);
  };
  return (
    <div className="@container/main flex flex-1 flex-col gap-2">
      <Toaster position="top-right" richColors closeButton />
      <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
        <div className="px-5 lg:px-6">
          <InputInline
            onStart={handleAnalyzeStart}
            onComplete={handleAnalyzeComplete}
          />

          <SectionCards
            total={stats.total}
            positive={stats.positive}
            negative={stats.negative}
            neutral={stats.neutral}
          />
          <div className="mt-6">
            <ChartAreaInteractive data={rawData} />

            <div className="mt-6">
              <DataTable data={rawData} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
