import { Badge } from "@/src/components/ui/badge";
import { Youtube, Twitter, Newspaper, Video } from "lucide-react";

export function HeroSection() {
  return (
    <div className="flex flex-col items-center text-center space-y-8 max-w-4xl mx-auto py-12">
      <div className="space-y-4">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-foreground bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">
          Welcome to Sentiment APPS
        </h1>

        <p className="max-w-2xl text-xl text-muted-foreground leading-relaxed mx-auto">
          Search any keyword and get instant sentiment analysis results across multiple platforms.
        </p>
      </div>

      <div className="flex flex-col items-center gap-3">
        <span className="text-xs font-semibold text-muted-foreground uppercase tracking-widest">
          Supported Platforms
        </span>
        <div className="flex items-center gap-3">
          <Badge variant="outline" className="px-3 py-1 flex gap-2 items-center text-sm font-medium hover:bg-muted transition-colors">
            <Twitter className="w-4 h-4 text-blue-400" />
            Twitter
          </Badge>
          <Badge variant="outline" className="px-3 py-1 flex gap-2 items-center text-sm font-medium hover:bg-muted transition-colors">
            <Youtube className="w-4 h-4 text-red-500" />
            YouTube
          </Badge>
          <Badge variant="outline" className="px-3 py-1 flex gap-2 items-center text-sm font-medium hover:bg-muted transition-colors">
            <Video className="w-4 h-4 text-pink-500" />
            TikTok
          </Badge>
          <Badge variant="outline" className="px-3 py-1 flex gap-2 items-center text-sm font-medium hover:bg-muted transition-colors">
            <Newspaper className="w-4 h-4 text-orange-500" />
            News
          </Badge>
        </div>
      </div>
    </div>
  );
}
