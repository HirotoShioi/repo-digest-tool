import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { X } from "lucide-react";

interface PatternListProps {
  patterns: string[];
  type: "exclude" | "include";
  onRemove: (pattern: string, type: "exclude" | "include") => void;
}

export function PatternList({ patterns, type, onRemove }: PatternListProps) {
  return (
    <ScrollArea className="h-[300px] rounded-md border p-4">
      <div className="flex flex-wrap gap-2">
        {patterns.map((pattern) => (
          <Badge
            key={pattern}
            variant="secondary"
            className="flex items-center gap-1"
          >
            {pattern}
            <button
              onClick={() => onRemove(pattern, type)}
              className="ml-1 hover:text-destructive"
              aria-label={`Remove ${pattern} pattern`}
            >
              <X className="h-3 w-3" />
            </button>
          </Badge>
        ))}
      </div>
    </ScrollArea>
  );
}
