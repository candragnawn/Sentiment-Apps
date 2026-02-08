"use client";

import * as React from "react";
import {
  ArrowUpCircleIcon,
  HistoryIcon,
  HouseHeartIcon,
  LayoutDashboardIcon,
  HelpCircleIcon,
  SearchIcon,
  SettingsIcon,
} from "lucide-react";

import { NavDocuments } from "@/src/components/nav-documents";
import Link from "next/link";
import { NavMain } from "@/src/components/nav-main";
import { NavSecondary } from "@/src/components/nav-secondary";
import { NavUser } from "@/src/components/nav-user";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/src/components/ui/sidebar";

const data = {
  user: {
    name: "Pakelpo",
    email: "m@example.com",
    avatar: "",
  },
  navMain: [
    {
      title: "Home",
      url: "/",
      icon: HouseHeartIcon,
    },
    {
      title: "Dashboard",
      url: "/dashboard",
      icon: LayoutDashboardIcon,
    },
    {
      title: "History",
      url: "/history",
      icon: HistoryIcon,
    },
  ],
  documents: [],
  navSecondary: [
    { title: "Settings", url: "#", icon: SettingsIcon },
    { title: "Get Help", url: "#", icon: HelpCircleIcon },
    { title: "Search", url: "#", icon: SearchIcon },
  ],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <Link href="/">
                <ArrowUpCircleIcon className="h-5 w-5" />
                <span className="text-base font-semibold">Sentiment App.</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent>
        <NavMain items={data.navMain} />
        <NavDocuments items={data.documents} />
        <NavSecondary items={data.navSecondary} className="mt-auto" />
      </SidebarContent>

      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
    </Sidebar>
  );
}
