"use client";

import { cn } from "@/lib/utils";

interface PageContainerProps {
  children: React.ReactNode;
  sidebarCollapsed?: boolean;
  className?: string;
}

export function PageContainer({
  children,
  sidebarCollapsed = false,
  className,
}: PageContainerProps) {
  return (
    <main
      className={cn(
        "min-h-screen pt-16 transition-[padding] duration-300 ease-in-out",
        sidebarCollapsed ? "lg:pl-[68px]" : "lg:pl-[240px]",
        className,
      )}
    >
      <div className="mx-auto max-w-7xl px-4 py-8 lg:px-8">{children}</div>
    </main>
  );
}
