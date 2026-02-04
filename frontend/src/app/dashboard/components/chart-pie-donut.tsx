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
} from "@/src/app/dashboard/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/src/app/dashboard/components/ui/chart"
import { positive } from "zod"

export const description = "A donut chart"

const chartData = [
  { browser: "chrome", visitors: 275, fill: "var(--color-chrome)" },
  { browser: "safari", visitors: 200, fill: "var(--color-safari)" },
  { browser: "firefox", visitors: 187, fill: "var(--color-firefox)" },
  { browser: "edge", visitors: 173, fill: "var(--color-edge)" },
  { browser: "other", visitors: 90, fill: "var(--color-other)" },
]

const chartConfig = {
  positive: {
    label: "Positive",
    color: "hsl(var(--chart-1))",
  },
  negative: {
    label: "Negative",
    color: "hsl(var(--chart-2))",
  },
  neutral: {
    label: "Neutral",
    color: "hsl(var(--chart-3))",
  },
  news: {
    label: "News",
    color: "hsl(var(--chart-4))",
  },
  twitter: {
    label: "Twitter",
    color: "hsl(var(--chart-5))",
  },
  tiktok: {
    label: "Tiktok",
    color: "hsl(var(--chart-6))",
  },
  youtube: {
    label: "Youtube",
    color: "hsl(var(--chart-7))",
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
              innerRadius={80}
            />
          </PieChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col gap-2 text-sm">
        {footer}
      </CardFooter>
    </Card>
  )
}
