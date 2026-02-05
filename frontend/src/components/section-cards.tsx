"use client";
import { TrendingDownIcon, TrendingUpIcon, MessageSquareIcon, SmileIcon, FrownIcon, BarChart3Icon } from "lucide-react"

import { Badge } from "@/src/components/ui/badge"
import {
  Card,
  CardFooter,
  CardHeader,
  CardTitle,
  CardDescription
} from "@/src/components/ui/card"

interface SectionCardsProps {
  total: number;
  positive: number;
  negative: number;
  neutral: number;
}

export function SectionCards({ total, positive, negative, neutral }: SectionCardsProps) {
  return (
    <div className="*:data-[slot=card]:shadow-xs @xl/main:grid-cols-2 @5xl/main:grid-cols-4 grid grid-cols-1 gap-4 px-4 *:data-[slot=card]:bg-gradient-to-t *:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card dark:*:data-[slot=card]:bg-card lg:px-6">
      
   
      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>Total Mentions</CardDescription>
          <CardTitle className="@[250px]/card:text-3xl text-2xl font-semibold tabular-nums">
            {total.toLocaleString()} 
          </CardTitle>
          <div className="absolute right-4 top-4 text-zinc-500">
             <MessageSquareIcon className="size-5" />
          </div>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="text-muted-foreground">Total data dianalisis</div>
        </CardFooter>
      </Card>

      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>Positive Feedback</CardDescription>
          <CardTitle className="@[250px]/card:text-3xl text-2xl font-semibold tabular-nums ">
            {positive.toLocaleString()}
          </CardTitle>
          <div className="absolute right-4 top-4">
            <Badge variant="outline" className="flex gap-1 rounded-lg text-xs">
              <SmileIcon className="size-3" />
              Good
            </Badge>
          </div>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="text-muted-foreground">Sentimen Positif</div>
        </CardFooter>
      </Card>

  
      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>Negative Feedback</CardDescription>
          <CardTitle className="@[250px]/card:text-3xl text-2xl font-semibold tabular-num">
            {negative.toLocaleString()}
          </CardTitle>
          <div className="absolute right-4 top-4">
            <Badge variant="outline" className="flex gap-1 rounded-lg text-xs">
              <FrownIcon className="size-3" />
              Bad
            </Badge>
          </div>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="text-muted-foreground">Sentimen Negatif</div>
        </CardFooter>
      </Card>

     
      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>Neutral</CardDescription>
          <CardTitle className="@[250px]/card:text-3xl text-2xl font-semibold tabular-nums">
            {neutral.toLocaleString()}
          </CardTitle>
          <div className="absolute right-4 top-4 text-zinc-500">
             <BarChart3Icon className="size-5" />
          </div>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="text-muted-foreground">Sentimen Netral</div>
        </CardFooter>
      </Card>

    </div>
  )
}