import { AppSidebar } from "@/src/app/dashboard/components/app-sidebar";
import { SiteHeader } from "@/src/app/dashboard/components/site-header";
import { ThemeProvider } from "@/src/app/dashboard/components/theme-provider";
import {
  SidebarInset,
  SidebarProvider,
} from "@/src/app/dashboard/components/ui/sidebar";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader />
        <div className="flex flex-1 flex-col">{children}</div>
      </SidebarInset>
    </SidebarProvider>
  );
}
