export function HeroSection({ data, isAnalyzing }: { data: any, isAnalyzing: boolean }) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6 backdrop-blur-md">
      <p className="text-xs font-medium text-zinc-500 uppercase tracking-widest">Latest Analysis</p>
      <h2 className="text-3xl font-bold mt-1">
        {isAnalyzing ? "Analyzing Data..." : data.keyword || "No Keyword"}
      </h2>
      <div className="mt-4 flex items-center gap-4">
        <div className={`rounded-full px-3 py-1 text-xs font-bold uppercase ${
          data.label === 'positive' ? 'bg-green-500/20 text-green-500' : 
          data.label === 'negative' ? 'bg-red-500/20 text-red-500' : 'bg-zinc-500/20 text-zinc-400'
        }`}>
          {isAnalyzing ? "Processing" : data.label}
        </div>
        <span className="text-zinc-400 text-sm">
           Confidence: {(data.score * 100).toFixed(1)}%
        </span>
      </div>
    </div>
  );
}