import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useFilterSettings } from "@/contexts/FilterSettingsContext";

export function AdvancedTab() {
  const { maxFileSize, setMaxFileSize, handleSave } = useFilterSettings();
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-medium">File Size Limit</h3>
        <p className="text-sm text-muted-foreground">
          Set the maximum file size that will be processed (in MB)
        </p>
      </div>
      <div className="flex gap-2">
        <Input
          type="number"
          value={maxFileSize}
          onChange={(e) => setMaxFileSize(Number(e.target.value))}
          className="max-w-xs"
          placeholder="Maximum file size (MB)"
        />
        <Button onClick={handleSave}>Save</Button>
      </div>
    </div>
  );
}
