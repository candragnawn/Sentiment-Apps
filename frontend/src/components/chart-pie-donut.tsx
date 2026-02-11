"use client"

import { TrendingUp } from "lucide-react"
import { Pie, PieChart } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/src/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/src/components/ui/chart"
import { positive } from "zod"

export const description = "A donut chart"



const chartConfig = {
  positive: {
    label: "Positive",
    color: "hsl(var(--chart-2))",
  },
  negative: {
    label: "Negative",
    color: "hsl(var(--chart-4))",
  },
  neutral: {
    label: "Neutral",
    color: "hsl(var(--chart-3))",
  },
  news: {
    label: "News",
    color: "hsl(var(--chart-2))",
  },
  twitter: {
    label: "Twitter",
    color: "hsl(var(--chart-2))",
  },
  tiktok: {
    label: "Tiktok",
    color: "hsl(var(--chart-3))",
  },
  youtube: {
    label: "Youtube",
    color: "hsl(var(--chart-4))",
  }
   
} satisfies ChartConfig

export function ChartPieDonut({title, description, chartData, footer}: any) {
  return (
    <Card className="flex flex-col w-full ">
      <CardHeader className="items-center pb-0">
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <ChartContainer
          config={chartConfig}
          className="mx-auto aspect-square max-h-[280px]"
        >
          <PieChart>
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Pie
              data={chartData}
              dataKey="value" 
              nameKey="label"
              innerRadius={75}
            />
          </PieChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col gap-2 text-lg">
        {footer}
      </CardFooter>
    </Card>
  )
}
