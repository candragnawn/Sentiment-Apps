"use client";
import { InputInline } from "@/src/components/search";
import React from "react";
import { SectionCards } from "../components/section-cards";

export default function HomePage() {
  return (
    <div className="@container/main p-64 bg-background h-screen p-4">
      <div className="item-center content-center bg-card p-8">
        <h2 className=" text-center items-center justify-start text-[48px] justify-center text-white">
          Welcome to Sentimen apps
        </h2>
        <p className="text-center"> sentiment application from keyword </p>
      </div>
    </div>
  );
}
