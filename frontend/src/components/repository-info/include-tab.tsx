import { Button } from "@/components/ui/button";
import { PatternInput } from "./pattern-input";
import { PatternList } from "./pattern-list";
import { useFilterSettings } from "@/contexts/filter-settings-context";
import { useState, useCallback } from "react";
import { Minimatch } from "minimatch";
import { useToast } from "@/hooks/use-toast";

function isValidGlob(pattern: string): boolean {
  if (!pattern || pattern.trim().length === 0) return false;

  try {
    new Minimatch(pattern);
    return true;
  } catch {
    return false;
  }
}

export function IncludeTab() {
  const { filterSettings, handleSavePatterns } = useFilterSettings();
  const { toast } = useToast();
  const [patterns, setPatterns] = useState<string[]>(filterSettings.includePatterns);
  const [newPattern, setNewPattern] = useState("");

  const showErrorToast = useCallback(() => {
    toast({
      title: "Invalid Pattern",
      description: "Pattern is empty, invalid or already exists.",
      variant: "destructive",
    });
  }, [toast]);

  const handleAdd = useCallback(() => {
    const trimmedPattern = newPattern.trim();
    if (
      trimmedPattern &&
      isValidGlob(trimmedPattern) &&
      !patterns.includes(trimmedPattern)
    ) {
      setPatterns((prev) => [...prev, trimmedPattern]);
      setNewPattern("");
    } else {
      showErrorToast();
    }
  }, [newPattern, patterns, showErrorToast]);

  const handleRemove = useCallback((pattern: string) => {
    setPatterns((prev) => prev.filter((p) => p !== pattern));
  }, []);

  const handleSave = useCallback(() => {
    handleSavePatterns({
      includePatterns: patterns,
      excludePatterns: filterSettings.excludePatterns,
    });
  }, [handleSavePatterns, patterns, filterSettings.excludePatterns]);

  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-medium">Include Patterns</h3>
        <p className="text-sm text-muted-foreground">
          Specify patterns for files that should always be included
        </p>
      </div>
      <PatternInput
        value={newPattern}
        onChange={setNewPattern}
        onAdd={handleAdd}
        placeholder="Add new include pattern (e.g. *.md)"
      />
      <PatternList patterns={patterns} type="include" onRemove={handleRemove} />
      <div className="flex justify-end mt-4">
        <Button onClick={handleSave}>Save Settings</Button>
      </div>
    </div>
  );
}
