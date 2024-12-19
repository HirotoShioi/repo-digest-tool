import { Button } from "@/components/ui/button";
import { useFilterSettings } from "@/contexts/FilterSettingsContext";
import { PatternInput } from "@/pages/RepositoryDetails/components/PatternInput";
import { PatternList } from "@/pages/RepositoryDetails/components/PatternList";

export function ExcludeTab() {
  const {
    newExcludePattern,
    setNewExcludePattern,
    excludePatterns,
    addPattern,
    removePattern,
    handleSave,
  } = useFilterSettings();
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-medium">Exclude Patterns</h3>
        <p className="text-sm text-muted-foreground">
          Specify patterns for files and directories to exclude from processing
        </p>
      </div>
      <PatternInput
        value={newExcludePattern}
        onChange={setNewExcludePattern}
        onAdd={() => addPattern("exclude")}
        placeholder="Add new exclude pattern (e.g. *.log)"
      />
      <PatternList
        patterns={excludePatterns}
        type="exclude"
        onRemove={(pattern) => removePattern(pattern, "exclude")}
      />
      <div className="flex justify-end mt-4">
        <Button onClick={handleSave}>Save Settings</Button>
      </div>
    </div>
  );
}
