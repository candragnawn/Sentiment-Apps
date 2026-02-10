import { Button } from "@/src/components/ui/button";
import { ArrowRight } from "lucide-react";

export function HeroSection() {
  return (
    <div className="flex flex-col items-center text-center space-y-6 max-w-4xl mx-auto py-12">
  
      

    
      <h1 className="text-2xl md:text-6xl lg:text-4xl font-bold tracking-tight text-foreground">
        Welcome to Sentiment APPS
      </h1>

      <p className="max-w-2xl text-lg md:text-xl text-muted-foreground leading-relaxed">
        Clean, modern building blocks. Copy and paste into your apps.
        Works with all React frameworks. Open Source. Free forever.
      </p>

    </div>
  );
}
