import { Textarea } from "@/components/ui/textarea";

interface AITabProps {
  aiPrompt: string;
  setAiPrompt: (value: string) => void;
}

export function AITab({ aiPrompt, setAiPrompt }: AITabProps) {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-medium">AI</h3>
        <p className="text-sm text-muted-foreground">
          AI will try to only include files that are relevant.
        </p>
      </div>
      <Textarea
        className="max-w-xs"
        placeholder="AI prompt"
        value={aiPrompt}
        onChange={(e) => setAiPrompt(e.target.value)}
      />
    </div>
  );
}
