"use client";

import { useState, useEffect } from "react";
import { Plus, X } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

const defaultPatterns = [
  "__pycache__/",
  "*.pyc",
  "*.log",
  ".git/*",
  ".gptignore",
  "LICENSE",
  ".github/*",
  ".tox/*",
  ".mypy_cache/*",
  "*.whl",
  "*.tar",
  "*.tar.gz",
  ".gitignore",
  "*.env*",
  "*.png",
  "*.jpeg",
  "*.jpg",
  "*bin/*",
  "*.svg",
  "*.pdf",
  "*.mp4",
  "*.webp",
  "*.sketch",
  "pnpm-lock.yaml",
  "*.ico",
  "yarn.lock",
  "docs/**",
  "bun.lockb",
  "benchmarks/**",
  "*.test.ts",
  "*.test.tsx",
];

function SettingsPage() {
  const [excludePatterns, setExcludePatterns] =
    useState<string[]>(defaultPatterns);
  const [includePatterns, setIncludePatterns] = useState<string[]>([]);
  const [maxFileSize, setMaxFileSize] = useState<number>(10);
  const [newPattern, setNewPattern] = useState("");

  useEffect(() => {
    // Here you would typically fetch the current settings from an API or local storage
    // For now, we'll use the default patterns
  }, []);

  const addPattern = (type: "exclude" | "include") => {
    const trimmedPattern = newPattern.trim();
    if (trimmedPattern) {
      if (type === "exclude") {
        setExcludePatterns((prev) => [...prev, trimmedPattern]);
      } else {
        setIncludePatterns((prev) => [...prev, trimmedPattern]);
      }
      setNewPattern("");
    }
  };

  const removePattern = (pattern: string, type: "exclude" | "include") => {
    if (type === "exclude") {
      setExcludePatterns((prev) => prev.filter((p) => p !== pattern));
    } else {
      setIncludePatterns((prev) => prev.filter((p) => p !== pattern));
    }
  };

  const handleSave = async () => {
    // Here you would typically save the settings to an API or local storage
    console.log("Exclude Patterns:", excludePatterns);
    console.log("Include Patterns:", includePatterns);
    console.log("Max File Size:", maxFileSize);
    // TODO: Implement actual save functionality
  };

  const PatternList = ({
    patterns,
    type,
  }: {
    patterns: string[];
    type: "exclude" | "include";
  }) => (
    <ScrollArea className="h-[200px] rounded-md border p-4">
      <div className="flex flex-wrap gap-2">
        {patterns.map((pattern) => (
          <Badge
            key={pattern}
            variant="secondary"
            className="flex items-center gap-1"
          >
            {pattern}
            <button
              onClick={() => removePattern(pattern, type)}
              className="ml-1 hover:text-destructive"
              aria-label={`Remove ${pattern} pattern`}
            >
              <X className="h-3 w-3" />
            </button>
          </Badge>
        ))}
      </div>
    </ScrollArea>
  );

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Filter Settings</h1>
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Exclude Patterns</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-2 mb-4">
              <Input
                placeholder="Add new exclude pattern (e.g. *.log)"
                value={newPattern}
                onChange={(e) => setNewPattern(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addPattern("exclude")}
              />
              <Button onClick={() => addPattern("exclude")} size="icon">
                <Plus className="h-4 w-4" />
              </Button>
            </div>
            <PatternList patterns={excludePatterns} type="exclude" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Include Patterns</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-2 mb-4">
              <Input
                placeholder="Add new include pattern (e.g. *.md)"
                value={newPattern}
                onChange={(e) => setNewPattern(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addPattern("include")}
              />
              <Button onClick={() => addPattern("include")} size="icon">
                <Plus className="h-4 w-4" />
              </Button>
            </div>
            <PatternList patterns={includePatterns} type="include" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>File Size Limit</CardTitle>
          </CardHeader>
          <CardContent>
            <Input
              type="number"
              value={maxFileSize}
              onChange={(e) => setMaxFileSize(Number(e.target.value))}
              className="w-full"
              placeholder="Maximum file size (MB)"
            />
          </CardContent>
        </Card>

        <Button onClick={handleSave} className="w-full">
          Save Settings
        </Button>
      </div>
    </div>
  );
}

export default SettingsPage;
