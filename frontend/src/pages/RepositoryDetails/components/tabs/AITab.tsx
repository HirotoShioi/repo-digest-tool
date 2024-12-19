import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useFilterSettings } from "@/contexts/FilterSettingsContext";
import { useState } from "react";

export function AITab() {
  const { onSave } = useFilterSettings();
  const [aiPrompt, setAiPrompt] = useState<string>("");
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-medium">AI</h3>
        <p className="text-sm text-muted-foreground">
          AI will try to only include files that are relevant.
        </p>
      </div>
      <Textarea
        className="w-full resize-none"
        placeholder="Please describe the files you want to include"
        data-virtualkeyboard="true"
        value={aiPrompt}
        onChange={(e) => setAiPrompt(e.target.value)}
        rows={10}
      />
      <div className="flex justify-end">
        <Button onClick={onSave}>Start</Button>
      </div>
    </div>
  );
}
