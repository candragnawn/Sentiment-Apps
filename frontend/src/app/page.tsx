"use client";
import React from "react";
import { HeroSection } from "@/src/components/hero-section";
import { InputInline } from "@/src/components/search";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/src/components/ui/card";
import { Badge } from "@/src/components/ui/badge";
import { BarChart3, Cloud, LayoutDashboard, TrendingUp } from "lucide-react";

const FeatureCard = ({
  icon: Icon,
  title,
  description,
}: {
  icon: any;
  title: string;
  description: string;
}) => (
  <Card className="bg-card/50 backdrop-blur-sm border-border/50 transition-all hover:bg-card hover:shadow-md">
    <CardHeader>
      <div className="p-2 w-fit rounded-lg bg-primary/10 mb-2">
        <Icon className="w-6 h-6 text-primary" />
      </div>
      <CardTitle className="text-lg">{title}</CardTitle>
    </CardHeader>
    <CardContent>
      <CardDescription>{description}</CardDescription>
    </CardContent>
  </Card>
);

export default function HomePage() {
  const trendingKeywords = [
    "Pilpres 2024",
    "iPhone 15",
    "Crypto",
    "Timnas Indonesia",
    "AI Technology"
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-100px)] p-6 bg-background space-y-12">
      <div className="w-full max-w-5xl flex flex-col items-center justify-center">
        <div className="w-full max-w-4xl flex flex-col items-center py-16 px-10 bg-card/50 backdrop-blur-sm rounded-3xl border border-border/50 shadow-xl transition-all hover:shadow-2xl space-y-12">
          <HeroSection />

          <div className="w-full max-w-2xl flex flex-col items-center space-y-6">
            <div className="w-full flex justify-center">
              <InputInline />
            </div>

            <div className="flex flex-wrap items-center justify-center gap-2 text-sm text-muted-foreground">
              <span className="flex items-center gap-1 font-medium">
                <TrendingUp className="w-4 h-4" /> Trending:
              </span>
              {trendingKeywords.map((keyword) => (
                <Badge
                  key={keyword}
                  variant="secondary"
                  className="cursor-pointer hover:bg-secondary/80 transition-colors"
                >
                  {keyword}
                </Badge>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="w-full max-w-5xl grid grid-cols-1 md:grid-cols-3 gap-6">
        <FeatureCard
          icon={BarChart3}
          title="Sentiment Analysis"
          description="Analyze the emotional tone of text data to understand positive, negative, and neutral sentiments."
        />
        <FeatureCard
          icon={Cloud}
          title="Word Cloud"
          description="Visualize the most frequent words in a dataset to quickly identify key themes and topics."
        />
        <FeatureCard
          icon={LayoutDashboard}
          title="Multi-Platform"
          description="Gather insights from various social media platforms like Twitter, YouTube, and TikTok in one place."
        />
      </div>
    </div>
  );
}
