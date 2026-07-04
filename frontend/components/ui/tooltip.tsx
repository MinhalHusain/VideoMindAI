"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

function Tooltip({
  children,
  content,
  side = "right",
  className,
}: {
  children: React.ReactNode;
  content: string;
  side?: "top" | "right" | "bottom" | "left";
  className?: string;
}) {
  return (
    <div className={cn("group relative inline-flex", className)}>
      {children}
      <div
        role="tooltip"
        className={cn(
          "pointer-events-none absolute z-50 hidden whitespace-nowrap rounded-md bg-primary px-3 py-1.5 text-xs text-primary-foreground shadow-md group-hover:block",
          side === "right" && "left-full top-1/2 ml-2 -translate-y-1/2",
          side === "left" && "right-full top-1/2 mr-2 -translate-y-1/2",
          side === "top" && "bottom-full left-1/2 mb-2 -translate-x-1/2",
          side === "bottom" && "top-full left-1/2 mt-2 -translate-x-1/2",
        )}
      >
        {content}
      </div>
    </div>
  );
}

export { Tooltip };
