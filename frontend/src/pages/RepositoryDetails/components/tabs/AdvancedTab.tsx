import { Input } from "@/components/ui/input";

interface AdvancedTabProps {
  maxFileSize: number;
  setMaxFileSize: (value: number) => void;
}

export function AdvancedTab({ maxFileSize, setMaxFileSize }: AdvancedTabProps) {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-medium">File Size Limit</h3>
        <p className="text-sm text-muted-foreground">
          Set the maximum file size that will be processed (in MB)
        </p>
      </div>
      <Input
        type="number"
        value={maxFileSize}
        onChange={(e) => setMaxFileSize(Number(e.target.value))}
        className="max-w-xs"
        placeholder="Maximum file size (MB)"
      />
    </div>
  );
}
