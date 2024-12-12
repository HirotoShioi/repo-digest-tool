"use client";
import { useState, useEffect } from 'react';
import { Plus, X } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useGetSettings } from "@/services/settings/queries";
import { useUpdateSettings } from "@/services/settings/mutations";
import { useToast } from "@/hooks/use-toast";
import { useQueryClient } from "@tanstack/react-query";

interface FilterSettingDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function FilterSettingDialog({ open, onOpenChange }: FilterSettingDialogProps) {
  const { data: filterSettings } = useGetSettings();
  const queryClient = useQueryClient();
  const { toast } = useToast();

  const [excludePatterns, setExcludePatterns] = useState<string[]>([]);
  const [includePatterns, setIncludePatterns] = useState<string[]>([]);
  const [maxFileSize, setMaxFileSize] = useState<number>(10);
  const [newExcludePattern, setNewExcludePattern] = useState("");
  const [newIncludePattern, setNewIncludePattern] = useState("");

  // データ取得後、一度だけローカルステートに反映
  useEffect(() => {
    if (filterSettings) {
      setExcludePatterns(filterSettings.excludePatterns || []);
      setIncludePatterns(filterSettings.includePatterns || []);
      // maxFileSizeがserverから来るならここでセット
    }
  }, [filterSettings]);

  function addPattern(type: "exclude" | "include") {
    if (type === "exclude") {
      const trimmedPattern = newExcludePattern.trim();
      if (trimmedPattern) {
        setExcludePatterns((prev) => [...prev, trimmedPattern]);
        setNewExcludePattern("");
      }
    } else {
      const trimmedPattern = newIncludePattern.trim();
      if (trimmedPattern) {
        setIncludePatterns((prev) => [...prev, trimmedPattern]);
        setNewIncludePattern("");
      }
    }
  }

  function removePattern(pattern: string, type: "exclude" | "include") {
    if (type === "exclude") {
      setExcludePatterns((prev) => prev.filter((p) => p !== pattern));
    } else {
      setIncludePatterns((prev) => prev.filter((p) => p !== pattern));
    }
  }

  const { mutate: updateSettings } = useUpdateSettings();

  async function handleSave() {
    updateSettings(
      {
        includePatterns,
        excludePatterns,
      },
      {
        onSuccess: (newData) => {
          // サーバー更新成功後にキャッシュ更新
          queryClient.setQueryData(['settings'], newData);
          toast({
            title: "Settings updated",
            variant: "default",
            description: "Your settings have been updated successfully",
          });
          onOpenChange(false);
        },
      }
    );
  }

  function PatternList({
    patterns,
    type,
  }: {
    patterns: string[];
    type: "exclude" | "include";
  }) {
    return (
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
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Filter Settings</DialogTitle>
          <DialogDescription></DialogDescription>
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
                value={newExcludePattern}
                onChange={(e) => setNewExcludePattern(e.target.value)}
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
                value={newIncludePattern}
                onChange={(e) => setNewIncludePattern(e.target.value)}
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
