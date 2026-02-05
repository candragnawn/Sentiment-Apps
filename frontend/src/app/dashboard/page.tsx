"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { SectionCards } from "@/src/components/section-cards";
import { InputInline } from "@/src/components/search";
import { HeroSection } from "@/src/components/hero-section";
import { Toaster, toast } from "sonner";

const ChartAreaInteractive = dynamic(() => import("@/src/components/chart-area-interactive").then(mod => mod.ChartAreaInteractive), { ssr: false });
const DataTable = dynamic(() => import("@/src/components/data-table").then(mod => mod.DataTable), { ssr: false });


export default function DashboardPage() {
  const [rawData, setRawData] = useState<any[]>([]);
  const [stats, setStats] = useState({ total: 0, positive: 0, negative: 0, neutral: 0 });
  const [chartData, setChartData] = useState<any[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  const loadAllData = async () => {
    setLoading(true);
    try {
      const statsRes = await fetch("http://127.0.0.1:8000/api/sentiment/stats");
      const statsJson = await statsRes.json();
      setStats(statsJson);

      const chartRes = await fetch("http://127.0.0.1:8000/api/sentiment/chart?days=30");
      const chartJson = await chartRes.json();
      setChartData(chartJson);

      const listRes = await fetch(`http://127.0.0.1:8000/api/sentiment/list?days=30`);
      const listJson = await listRes.json();
      const rawRes = Array.isArray(listJson) ? listJson : listJson.data || [];
      
      const transformed = rawRes.map((item: any) => ({
        id: item.id,
        header: item.text_raw?.substring(0, 100) || item.keyword,
        type: `${item.author} (${item.platform})`,
        status: item.label === 'positive' ? 'Done' : 'In Progress',
        target: `${item.label} (${item.score}%)`,
        limit: item.published_date ? new Date(item.published_date).toLocaleDateString() : 'No Date',
        reviewer: item.keyword
      }));

      setRawData(transformed);
    } catch (error) {
      console.error("Failed to load data", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
    const interval = setInterval(() => {
      loadAllData();
    }, 15000); 
    return () => clearInterval(interval);
  }, []);


  const handleAnalyzeComplete = async () => {
    await loadAllData();
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
            <ChartAreaInteractive data={chartData} />

            <div className="mt-6">
              <DataTable data={rawData} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );

}
