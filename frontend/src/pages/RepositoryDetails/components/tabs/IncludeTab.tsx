import { PatternInput } from "../PatternInput";
import { PatternList } from "../PatternList";

interface IncludeTabProps {
  newIncludePattern: string;
  setNewIncludePattern: (value: string) => void;
  includePatterns: string[];
  onAdd: () => void;
  onRemove: (pattern: string, type: "exclude" | "include") => void;
}

export function IncludeTab({
  newIncludePattern,
  setNewIncludePattern,
  includePatterns,
  onAdd,
  onRemove,
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
    </div>
  );
}
