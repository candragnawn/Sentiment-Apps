"use client";
import { InputInline } from "@/src/components/search";
import React from "react";

export default function HomePage() {
  return (
    <div className="flex flex-1 items-center justify-center p-4">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Welcome to Sentiment App</h1>
        <p className="text-muted-foreground">User landing page design coming soon...</p>
        <div>
           <InputInline />
        </div>
      </div>
    </div>
  );
}
