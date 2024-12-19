import { Button } from "@/components/ui/button";
import { PatternInput } from "@/pages/RepositoryDetails/components/PatternInput";
import { PatternList } from "@/pages/RepositoryDetails/components/PatternList";

interface ExcludeTabProps {
  newExcludePattern: string;
  setNewExcludePattern: (value: string) => void;
  excludePatterns: string[];
  onAdd: () => void;
  onRemove: (pattern: string, type: "exclude" | "include") => void;
  onSave: () => void;
}

export function ExcludeTab({
  newExcludePattern,
  setNewExcludePattern,
  excludePatterns,
  onAdd,
  onRemove,
  onSave,
}: ExcludeTabProps) {
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
        onAdd={onAdd}
        placeholder="Add new exclude pattern (e.g. *.log)"
      />
      <PatternList
        patterns={excludePatterns}
        type="exclude"
        onRemove={onRemove}
      />
      <div className="flex justify-end mt-4">
        <Button onClick={onSave}>Save Settings</Button>
      </div>
    </div>
  );
}
