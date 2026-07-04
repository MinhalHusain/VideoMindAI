"use client";

import { useState } from "react";
import { Navbar, Sidebar, PageContainer } from "@/components/layout";

export function AppShell({ children }: { children: React.ReactNode }) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <>
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed((prev) => !prev)} />
      <Navbar />
      <PageContainer sidebarCollapsed={collapsed}>{children}</PageContainer>
    </>
  );
}
