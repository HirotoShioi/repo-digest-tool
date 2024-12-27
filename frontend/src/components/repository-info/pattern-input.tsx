import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

interface PatternInputProps {
  value: string;
  onChange: (value: string) => void;
  onAdd: () => void;
  placeholder: string;
}

export function PatternInput({
  value,
  onChange,
  onAdd,
  placeholder,
}: PatternInputProps) {
  return (
    <div className="flex gap-2 mb-2">
      <Input
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onAdd()}
      />
      <Button onClick={onAdd} size="icon">
        <Plus className="h-4 w-4" />
      </Button>
    </div>
  );
}
