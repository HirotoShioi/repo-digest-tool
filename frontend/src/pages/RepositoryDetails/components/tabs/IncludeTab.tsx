import { Button } from "@/components/ui/button";
import { PatternInput } from "../PatternInput";
import { PatternList } from "../PatternList";
import { useFilterSettings } from "@/contexts/FilterSettingsContext";

export function IncludeTab() {
  const {
    newIncludePattern,
    setNewIncludePattern,
    includePatterns,
    addPattern,
    removePattern,
    handleSave,
  } = useFilterSettings();
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-medium">Include Patterns</h3>
        <p className="text-sm text-muted-foreground">
          Specify patterns for files that should always be included
        </p>
      </div>
      <PatternInput
        value={newIncludePattern}
        onChange={setNewIncludePattern}
        onAdd={() => addPattern("include")}
        placeholder="Add new include pattern (e.g. *.md)"
      />
      <PatternList
        patterns={includePatterns}
        type="include"
        onRemove={(pattern) => removePattern(pattern, "include")}
      />
      <div className="flex justify-end mt-4">
        <Button onClick={handleSave}>Save Settings</Button>
      </div>
    </div>
  );
}
