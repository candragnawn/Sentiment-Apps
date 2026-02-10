"use client";

import { usePathname } from "next/navigation";
import { Separator } from "@/src/components/ui/separator";
import { SidebarTrigger } from "@/src/components/ui/sidebar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbList,
  BreadcrumbPage,
} from "@/src/components/ui/breadcrumb";
import { ModeToggle } from "@/src/components/mode-togle";
import { InputInline } from "./search";

const routeConfig: Record<string, string> = {
  "/": "Home",
  "/dashboard": "Dashboard",
  "/history": "History",
};

export function SiteHeader() {
  const pathname = usePathname();
  const currentTitle = routeConfig[pathname] || "Sentiment App";

  return (
    <header className="flex h-14 shrink-0 items-center justify-between  bg-card px-4 sticky top-0 z-50">
      <div className="flex items-center gap-2">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-2 h-4" />
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbPage className="text-base font-medium">
                {currentTitle}
              </BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
      </div>
      <div className="flex item-center justify-center ">
        <InputInline />
      </div>
      <div className="flex items-center p-8">
        <ModeToggle />
      </div>
    </header>
  );
}
