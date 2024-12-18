"use client";
import { useState, useEffect, memo, useCallback } from "react";
import { Plus, Settings, X } from "lucide-react";
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
  DialogTrigger,
} from "@/components/ui/dialog";
import { useGetSettings } from "@/services/settings/queries";
import { useUpdateSettings } from "@/services/settings/mutations";
import { useToast } from "@/hooks/use-toast";
import { Minimatch } from "minimatch";

interface FilterSettingDialogProps {
  onSave: () => void;
  author: string;
  repository: string;
}

function isValidGlob(pattern: string): boolean {
  if (!pattern || pattern.trim().length === 0) return false;

  try {
    // Minimatchインスタンスを作成してパターンを検証
    new Minimatch(pattern);
    return true;
  } catch {
    return false;
  }
}

const PatternInput = memo(function PatternInput({
  value,
  onChange,
  onAdd,
  placeholder,
}: {
  value: string;
  onChange: (value: string) => void;
  onAdd: () => void;
  placeholder: string;
}) {
  return (
    <div className="flex gap-2 mb-2">
      <Input
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onAdd()}
      />
      <Button onClick={onAdd} size="icon">
        <Plus className="h-4 w-4" />
      </Button>
    </div>
  );
});

const PatternList = memo(function PatternList({
  patterns,
  type,
  onRemove,
}: {
  patterns: string[];
  type: "exclude" | "include";
  onRemove: (pattern: string, type: "exclude" | "include") => void;
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
              onClick={() => onRemove(pattern, type)}
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
});

const FileSizeInput = memo(function FileSizeInput({
  value,
  onChange,
}: {
  value: number;
  onChange: (value: number) => void;
}) {
  return (
    <Input
      type="number"
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
      className="max-w-xs"
      placeholder="Maximum file size (MB)"
    />
  );
});

export function FilterSettingDialog({
  author,
  repository,
  onSave,
}: FilterSettingDialogProps) {
  const { data: filterSettings } = useGetSettings({
    author,
    repository,
  });
  const { toast } = useToast();
  const { mutate: updateSettings } = useUpdateSettings();

  const [excludePatterns, setExcludePatterns] = useState<string[]>([]);
  const [includePatterns, setIncludePatterns] = useState<string[]>([]);
  const [maxFileSize, setMaxFileSize] = useState<number>(10);
  const [newExcludePattern, setNewExcludePattern] = useState("");
  const [newIncludePattern, setNewIncludePattern] = useState("");

  useEffect(() => {
    if (filterSettings) {
      setExcludePatterns(filterSettings.excludePatterns || []);
      setIncludePatterns(filterSettings.includePatterns || []);
    }
  }, [filterSettings]);

  const showErrorToast = useCallback(() => {
    toast({
      title: "Invalid Pattern",
      description: "Pattern is empty, invalid or already exists.",
      variant: "destructive",
    });
  }, [toast]);

  const addPattern = useCallback(
    (type: "exclude" | "include") => {
      if (type === "exclude") {
        const trimmedPattern = newExcludePattern.trim();
        if (
          trimmedPattern &&
          isValidGlob(trimmedPattern) &&
          !excludePatterns.includes(trimmedPattern)
        ) {
          setExcludePatterns((prev) => [...prev, trimmedPattern]);
          setNewExcludePattern("");
        } else {
          showErrorToast();
        }
      } else {
        const trimmedPattern = newIncludePattern.trim();
        if (
          trimmedPattern &&
          isValidGlob(trimmedPattern) &&
          !includePatterns.includes(trimmedPattern)
        ) {
          setIncludePatterns((prev) => [...prev, trimmedPattern]);
          setNewIncludePattern("");
        } else {
          showErrorToast();
        }
      }
    },
    [
      newExcludePattern,
      newIncludePattern,
      excludePatterns,
      includePatterns,
      showErrorToast,
    ]
  );

  const removePattern = useCallback(
    (pattern: string, type: "exclude" | "include") => {
      if (type === "exclude") {
        setExcludePatterns((prev) => prev.filter((p) => p !== pattern));
      } else {
        setIncludePatterns((prev) => prev.filter((p) => p !== pattern));
      }
    },
    []
  );

  const handleSave = useCallback(async () => {
    updateSettings(
      {
        author,
        name: repository,
        settings: {
          includePatterns,
          excludePatterns,
          maxFileSize,
        },
      },
      {
        onSuccess: () => {
          toast({
            title: "Settings updated",
            variant: "default",
            description: "Your settings have been updated successfully",
          });
          onSave();
        },
      }
    );
  }, [
    updateSettings,
    author,
    repository,
    includePatterns,
    excludePatterns,
    maxFileSize,
    toast,
    onSave,
  ]);

  const handleExcludePatternChange = useCallback((value: string) => {
    setNewExcludePattern(value);
  }, []);

  const handleIncludePatternChange = useCallback((value: string) => {
    setNewIncludePattern(value);
  }, []);

  const handleMaxFileSizeChange = useCallback((value: number) => {
    setMaxFileSize(value);
  }, []);

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button
          size="lg"
          className="bg-primary hover:bg-primary/90"
          data-testid="filter-dialog-button"
        >
          <Settings className="w-4 h-4" />
          Filter
        </Button>
      </DialogTrigger>
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
                Specify patterns for files and directories to exclude from
                processing
              </p>
            </div>
            <PatternInput
              value={newExcludePattern}
              onChange={handleExcludePatternChange}
              onAdd={() => addPattern("exclude")}
              placeholder="Add new exclude pattern (e.g. *.log)"
            />
            <PatternList
              patterns={excludePatterns}
              type="exclude"
              onRemove={removePattern}
            />
          </div>

          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-medium">Include Patterns</h3>
              <p className="text-sm text-muted-foreground">
                Specify patterns for files that should always be included
              </p>
            </div>
            <PatternInput
              value={newIncludePattern}
              onChange={handleIncludePatternChange}
              onAdd={() => addPattern("include")}
              placeholder="Add new include pattern (e.g. *.md)"
            />
            <PatternList
              patterns={includePatterns}
              type="include"
              onRemove={removePattern}
            />
          </div>

          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-medium">File Size Limit</h3>
              <p className="text-sm text-muted-foreground">
                Set the maximum file size that will be processed (in MB)
              </p>
            </div>
            <FileSizeInput
              value={maxFileSize}
              onChange={handleMaxFileSizeChange}
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
