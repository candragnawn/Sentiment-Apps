"use client";

import WorldCloud from "react-d3-cloud";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/src/components/ui/card";

export function WordCloudCard({
  data,
}: {
  data: { text: string; value: number }[];
}) {
  return (
    <Card className="h-full card[--color-card]">
      <CardHeader>
        <CardTitle className="text-lg font-medium text-white">
          Top Keywords WordCloud
        </CardTitle>
      </CardHeader>
      <CardContent>
        <WorldCloud
          data={data}
          width={2500}
          height={600}
          font="inter"
          fontWeight="bold"
          fontSize={(word) => Math.log2(word.value + 1) * 20}
          spiral="rectangular"
          rotate={() => 0}
          padding={4}
          fill={(d, i) => {
            const colors = ["#3b82f6", "#60a5fa", "#93c5fd", "#ffffff"];
            return colors[i % colors.length];
          }}
        />
      </CardContent>
    </Card>
  );
}
