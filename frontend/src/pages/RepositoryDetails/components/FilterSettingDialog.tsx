"use client";

import { useState } from "react";
import { Plus, X } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useGetSettings } from "@/services/settings/queries";
import { useUpdateSettings } from "@/services/settings/mutations";

interface FilterSettingDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

// Move defaultPatterns from Settings/index.tsx
const defaultPatterns = [
  "__pycache__/",
  "*.pyc",
  // ... (same patterns as in Settings/index.tsx)
];

export function FilterSettingDialog({ open, onOpenChange }: FilterSettingDialogProps) {
  const {data: filterSettings} = useGetSettings()
  const excludePatterns = filterSettings?.excludePatterns || defaultPatterns
  const includePatterns = filterSettings?.includePatterns || []
  const [newPattern, setNewPattern] = useState("");
  const [maxFileSize, setMaxFileSize] = useState(10);
  const { mutate: updateSettings } = useUpdateSettings()

  // Same functions as Settings/index.tsx
  const addPattern = (type: "exclude" | "include") => {
    const trimmedPattern = newPattern.trim();
    if (trimmedPattern) {
      if (type === "exclude") {
        updateSettings({
          ...filterSettings,
          excludePatterns: [...excludePatterns, trimmedPattern],
        });
      } else {
        updateSettings({
          ...filterSettings,
          includePatterns: [...includePatterns, trimmedPattern],
        });
      }
      setNewPattern("");
    }
  };

  const removePattern = (pattern: string, type: "exclude" | "include") => {
    if (type === "exclude") {
      updateSettings({
        ...filterSettings,
        excludePatterns: excludePatterns.filter((p) => p !== pattern),
      });
    } else {
      updateSettings({
        ...filterSettings,
        includePatterns: includePatterns.filter((p) => p !== pattern),
      });
    }
  };

  const handleSave = async () => {
    // Save logic here
    console.log("Exclude Patterns:", excludePatterns);
    console.log("Include Patterns:", includePatterns);
    console.log("Max File Size:", maxFileSize);
    onOpenChange(false);
  };

  const PatternList = ({
    patterns,
    type,
  }: {
    patterns: string[];
    type: "exclude" | "include";
  }) => (
    <ScrollArea className="h-[150px] rounded-md border p-4">
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
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Filter Settings</DialogTitle>
        </DialogHeader>
        <div className="space-y-8">
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-medium">Exclude Patterns</h3>
              <p className="text-sm text-muted-foreground">
                Specify patterns for files and directories to exclude from processing
              </p>
            </div>
            <div className="flex gap-2 mb-2">
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
          </div>

          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-medium">Include Patterns</h3>
              <p className="text-sm text-muted-foreground">
                Specify patterns for files that should always be included
              </p>
            </div>
            <div className="flex gap-2 mb-2">
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
          </div>

          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-medium">File Size Limit</h3>
              <p className="text-sm text-muted-foreground">
                Set the maximum file size that will be processed (in MB)
              </p>
            </div>
            <Input
              type="number"
              value={maxFileSize}
              onChange={(e) => setMaxFileSize(Number(e.target.value))}
              className="max-w-xs"
              placeholder="Maximum file size (MB)"
            />
          </div>

          <Button onClick={handleSave} className="w-full">
            Save Settings
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
