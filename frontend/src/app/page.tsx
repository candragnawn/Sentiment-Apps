"use client";
import React from "react";
import { HeroSection } from "@/src/components/hero-section";
import { InputInline } from "@/src/components/search";

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-100px)] p-6 bg-background">
      <div className="w-full max-w-5xl flex flex-col items-center space-y-16">
        <HeroSection />

        <div className="w-full max-w-2xl flex flex-col items-center py-5 px-10 bg-card/50 backdrop-blur-sm rounded-3xl border border-border/50 shadow-xl transition-all hover:shadow-2xl">
          <p className="text-sm font-medium text-muted-foreground mb-6 uppercase tracking-widest">
            Analyze New Sentiment
          </p>
          <div className="w-full flex justify-center">
            <InputInline />
          </div>
        </div>
      </div>
    </div>
  );
}
