"use client";
import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { Switch } from "@/components/ui/switch";

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  return (
    <NextThemesProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </NextThemesProvider>
  );
}

export function ThemeToggle() {
  const [mounted, setMounted] = React.useState(false);
  const { theme, setTheme } = require("next-themes").useTheme();
  React.useEffect(() => setMounted(true), []);
  if (!mounted) return null;
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-muted-foreground">🌞</span>
      <Switch checked={theme === "dark"} onCheckedChange={() => setTheme(theme === "dark" ? "light" : "dark")} />
      <span className="text-xs text-muted-foreground">🌙</span>
    </div>
  );
} 