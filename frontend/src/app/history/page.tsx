"use client";

import { HistoryTable } from "@/src/components/history-table";
import { useEffect, useState } from "react";

export default function HistoryPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchHistory() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/sentiment/history", {
            cache: 'no-store'
        });
        const json = await response.json();
        setData(json);
      } catch (error) {
        console.error("Failed to fetch history:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchHistory();
  }, []);

  return (
    <div className="flex flex-1 flex-col gap-6 p-4 md:p-6 pt-0">
      <div className="flex flex-col gap-2">
        <h1 className="text-xl font-medium tracking-tight">History Analysis</h1>
        <p className="text-muted-foreground">Lihat riwayat pencarian dan analisis Anda sebelumnya.</p>
      </div>
      
      {loading ? (
        <div className="flex items-center justify-center min-h-[200px]">
             <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      ) : (
        <HistoryTable data={data} />
      )}
    </div>
  );
}
