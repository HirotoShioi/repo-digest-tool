import { Button } from "@/components/ui/button";
import { PatternInput } from "../PatternInput";
import { PatternList } from "../PatternList";

interface IncludeTabProps {
  newIncludePattern: string;
  setNewIncludePattern: (value: string) => void;
  includePatterns: string[];
  onAdd: () => void;
  onRemove: (pattern: string, type: "exclude" | "include") => void;
  onSave: () => void;
}

export function IncludeTab({
  newIncludePattern,
  setNewIncludePattern,
  includePatterns,
  onAdd,
  onRemove,
  onSave,
}: IncludeTabProps) {
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
        onAdd={onAdd}
        placeholder="Add new include pattern (e.g. *.md)"
      />
      <PatternList
        patterns={includePatterns}
        type="include"
        onRemove={onRemove}
      />
      <div className="flex justify-end mt-4">
        <Button onClick={onSave}>Save Settings</Button>
      </div>
    </div>
  );
}
