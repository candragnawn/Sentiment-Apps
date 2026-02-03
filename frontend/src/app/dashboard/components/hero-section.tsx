"use client";
import { Card, CardContent, CardHeader, CardTitle } from "@/src/app/dashboard/components/ui/card";
import { Badge } from "@/src/app/dashboard/components/ui/badge";
interface HeroSectionProps {
  latestResult: {
    keyword: string;
    sentiment: string;
    confidence?: number;
    summary?: string;
  } | null;
}
export function HeroSection({ latestResult }: HeroSectionProps) {
  if (!latestResult) return null;
  const isPositive = latestResult.sentiment.toLowerCase() === "positive";
  const isNegative = latestResult.sentiment.toLowerCase() === "negative";
  
  return (
    <Card className="bg-zinc-900 border-zinc-800 text-white mb-6">
      <CardHeader>
        <CardTitle className="text-lg text-zinc-400">Analysis Result</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-4">
          <h1 className="text-3xl font-bold">{latestResult.keyword}</h1>
          <Badge 
            variant={isPositive ? "default" : isNegative ? "destructive" : "secondary"}
            className="text-lg px-4 py-1"
          >
            {latestResult.sentiment}
          </Badge>
        </div>
        {latestResult.summary && (
          <p className="text-zinc-300 bg-zinc-800/50 p-4 rounded-lg">
            {latestResult.summary}
          </p>
        )}
      </CardContent>
    </Card>
  );
}