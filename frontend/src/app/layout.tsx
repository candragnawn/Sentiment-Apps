import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import {
  SidebarProvider,
  SidebarTrigger,
  SidebarInset,
} from "@/src/components/ui/sidebar";
import { AppSidebar } from "@/src/components/app-sidebar";
import { ThemeProvider } from "@/src/components/theme-provider";
import { InputInline } from "@/src/components/search";
import { SiteHeader } from "@/src/components/site-header";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Sentiment Analysis Dashboard",
  description: "Real-time sentiment analysis from social media",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <html lang="en" suppressHydrationWarning>
        <head />
        <body>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            {" "}
            <SidebarProvider defaultOpen={true}>
              <AppSidebar />
              <SidebarInset>
                <SiteHeader />
                <main className="flex-1 overflow-y-auto">{children}</main>
              </SidebarInset>
            </SidebarProvider>
          </ThemeProvider>
        </body>
      </html>
    </>
  );
}
