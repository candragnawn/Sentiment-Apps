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
        <CardTitle className="text-lg font-medium">
          Top Keywords WordCloud
        </CardTitle>
      </CardHeader>
      <CardContent>
        <WorldCloud
          data={data}
          width={1800}
          height={500}
          font="inter"
          fontWeight="bold"
          fontSize={(word) => Math.log2(word.value + 1) * 22 + 10}
          spiral="archimedean"
          rotate={() => 0}
          padding={2}
          fill={(d, i) => {
            const colors = ["#CBD5E1", "#64748B", ];
            return colors[i % colors.length];
          }}
        />
      </CardContent>
    </Card>
  );
}
