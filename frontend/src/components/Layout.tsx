import { Outlet, Link } from "react-router";
import { cn } from "@/lib/utils";
import { FileText, Moon, Sun } from "lucide-react";
import { Button } from "./ui/button";
import { useTheme } from "@/hooks/useTheme";
import githubIcon from "@/assets/github.svg";

export function Layout() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="min-h-screen bg-muted">
      <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="mx-auto">
          <div className="flex h-14 items-center justify-between px-4">
            {/* Left section */}
            <div className="flex items-center gap-4">
              <Link
                className={cn(
                  "flex items-center gap-2 font-semibold hover:opacity-80"
                )}
                to="/"
              >
                <FileText className="w-5 h-5" />
                <span>Repo Digest Tool</span>
              </Link>
            </div>
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setTheme(theme === "light" ? "dark" : "light")}
              >
                <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                <span className="sr-only">Toggle theme</span>
              </Button>
              <a
                href="https://github.com/HirotoShioi/repo-digest-tool"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Button variant="ghost" size="icon">
                  <img src={githubIcon} alt="GitHub" className="h-5 w-5" />
                  <span className="sr-only">GitHub repository</span>
                </Button>
              </a>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 py-4">
        <Outlet />
      </div>
    </div>
  );
}
