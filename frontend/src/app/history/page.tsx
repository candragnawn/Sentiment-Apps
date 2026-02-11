"use client";
import React from "react";

export default function HistoryPage() {
  return (
    <div className="flex flex-1 flex-col gap-6 p-4 md:p-6 pt-0">
      <div className="flex flex-col gap-2">
        <h1 className="text-xl font-medium tracking-tight">History Analysis</h1>
        <p className="text-muted-foreground">Lihat riwayat pencarian dan analisis Anda sebelumnya.</p>
      </div>
      <div className="border rounded-lg p-12 text-center text-muted-foreground border-dashed">
        Data riwayat akan muncul di sini (Segera Hadir)
      </div>
    </div>
  );
}
