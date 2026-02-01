import { AppSidebar } from "@/src/app/dashboard/components/app-sidebar";
import { ChartAreaInteractive } from "@/src/app/dashboard/components/chart-area-interactive";
import { DataTable } from "@/src/app/dashboard/components/data-table";
import { SectionCards } from "@/src/app/dashboard/components/section-cards";
import data from "@/src/app/dashboard/data.json";

export default function HomePage() {
  return (
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      <div className="@container/main flex flex-1 flex-col gap-4">
        <SectionCards />
        <div className="min-h-[100vh] flex-1 rounded-xl md:min-h-min">
           <ChartAreaInteractive />
        </div>
        <DataTable data={data} />
      </div>
    </div>
  );
}
