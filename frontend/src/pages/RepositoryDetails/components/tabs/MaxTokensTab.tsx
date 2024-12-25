import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useFilterSettings } from "@/contexts/FilterSettingsContext";
import { useState, useEffect, useCallback } from "react";

export function MaxTokensTab() {
  const { initialSettings, handleSaveSize } = useFilterSettings();
  const [maxTokens, setMaxTokens] = useState(10);

  useEffect(() => {
    if (initialSettings) {
      setMaxTokens(initialSettings.maxTokens || 10);
    }
  }, [initialSettings]);

  const handleSave = useCallback(() => {
    handleSaveSize({ maxTokens: maxTokens });
  }, [handleSaveSize, maxTokens]);

  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-medium">Max Tokens Filter</h3>
        <p className="text-sm text-muted-foreground">
          You can set the maximum number of tokens that will be processed for
          each file.
        </p>
      </div>
      <div className="flex gap-2">
        <Input
          type="number"
          value={maxTokens}
          onChange={(e) => setMaxTokens(Number(e.target.value))}
          className="max-w-xs"
          placeholder="Maximum tokens"
        />
        <Button onClick={handleSave}>Save</Button>
      </div>
    </div>
  );
}
