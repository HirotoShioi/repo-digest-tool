import { Button } from "@/components/ui/button";
import { useFilterSettings } from "@/contexts/FilterSettingsContext";
import { PatternInput } from "@/pages/RepositoryDetails/components/PatternInput";
import { PatternList } from "@/pages/RepositoryDetails/components/PatternList";
import { useState, useEffect, useCallback } from "react";
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

export function ExcludeTab() {
  const { initialSettings, handleSavePatterns } = useFilterSettings();
  const { toast } = useToast();
  const [patterns, setPatterns] = useState<string[]>([]);
  const [newPattern, setNewPattern] = useState("");

  useEffect(() => {
    if (initialSettings) {
      setPatterns(initialSettings.excludePatterns || []);
    }
  }, [initialSettings]);

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
      excludePatterns: patterns,
      includePatterns: initialSettings?.includePatterns || [],
    });
  }, [handleSavePatterns, patterns, initialSettings?.includePatterns]);

  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-medium">Exclude Patterns</h3>
        <p className="text-sm text-muted-foreground">
          Specify patterns for files and directories to exclude from processing
        </p>
      </div>
      <PatternInput
        value={newPattern}
        onChange={setNewPattern}
        onAdd={handleAdd}
        placeholder="Add new exclude pattern (e.g. *.log)"
      />
      <PatternList patterns={patterns} type="exclude" onRemove={handleRemove} />
      <div className="flex justify-end mt-4">
        <Button onClick={handleSave}>Save Settings</Button>
      </div>
    </div>
  );
}
