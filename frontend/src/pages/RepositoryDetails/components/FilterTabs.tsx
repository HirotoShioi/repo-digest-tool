import { useState, useCallback, useEffect } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useGetSettings } from "@/services/settings/queries";
import { useUpdateSettings } from "@/services/settings/mutations";
import { useToast } from "@/hooks/use-toast";
import { Minimatch } from "minimatch";
import { ExcludeTab } from "./tabs/ExcludeTab";
import { IncludeTab } from "./tabs/IncludeTab";
import { AITab } from "./tabs/AITab";
import { AdvancedTab } from "./tabs/AdvancedTab";

interface FilterTabsProps {
  onSave: () => void;
  author: string;
  repository: string;
}

function isValidGlob(pattern: string): boolean {
  if (!pattern || pattern.trim().length === 0) return false;

  try {
    new Minimatch(pattern);
    return true;
  } catch {
    return false;
  }
}

function TabItem({
  value,
  children,
}: {
  value: string;
  children: React.ReactNode;
}) {
  return (
    <TabsTrigger
      value={value}
      className="justify-start px-3 py-2 hover:bg-muted/80 data-[state=active]:bg-muted w-[120px]"
    >
      {children}
    </TabsTrigger>
  );
}

export function FilterTabs({ author, repository, onSave }: FilterTabsProps) {
  const { data: filterSettings } = useGetSettings({
    author,
    repository,
  });
  const { toast } = useToast();
  const { mutate: updateSettings } = useUpdateSettings();

  const [excludePatterns, setExcludePatterns] = useState<string[]>([]);
  const [includePatterns, setIncludePatterns] = useState<string[]>([]);
  const [maxFileSize, setMaxFileSize] = useState<number>(10);
  const [aiPrompt, setAiPrompt] = useState<string>("");
  const [newExcludePattern, setNewExcludePattern] = useState("");
  const [newIncludePattern, setNewIncludePattern] = useState("");

  useEffect(() => {
    if (filterSettings) {
      setExcludePatterns(filterSettings.excludePatterns || []);
      setIncludePatterns(filterSettings.includePatterns || []);
      setMaxFileSize(filterSettings.maxFileSize || 10);
      setAiPrompt(filterSettings.aiPrompt || "");
    }
  }, [filterSettings]);

  const showErrorToast = useCallback(() => {
    toast({
      title: "Invalid Pattern",
      description: "Pattern is empty, invalid or already exists.",
      variant: "destructive",
    });
  }, [toast]);

  const addPattern = useCallback(
    (type: "exclude" | "include") => {
      if (type === "exclude") {
        const trimmedPattern = newExcludePattern.trim();
        if (
          trimmedPattern &&
          isValidGlob(trimmedPattern) &&
          !excludePatterns.includes(trimmedPattern)
        ) {
          setExcludePatterns((prev) => [...prev, trimmedPattern]);
          setNewExcludePattern("");
        } else {
          showErrorToast();
        }
      } else {
        const trimmedPattern = newIncludePattern.trim();
        if (
          trimmedPattern &&
          isValidGlob(trimmedPattern) &&
          !includePatterns.includes(trimmedPattern)
        ) {
          setIncludePatterns((prev) => [...prev, trimmedPattern]);
          setNewIncludePattern("");
        } else {
          showErrorToast();
        }
      }
    },
    [
      newExcludePattern,
      newIncludePattern,
      excludePatterns,
      includePatterns,
      showErrorToast,
    ]
  );

  const removePattern = useCallback(
    (pattern: string, type: "exclude" | "include") => {
      if (type === "exclude") {
        setExcludePatterns((prev) => prev.filter((p) => p !== pattern));
      } else {
        setIncludePatterns((prev) => prev.filter((p) => p !== pattern));
      }
    },
    []
  );

  const handleSave = useCallback(() => {
    updateSettings(
      {
        author,
        name: repository,
        settings: {
          includePatterns,
          excludePatterns,
          maxFileSize,
          aiPrompt,
        },
      },
      {
        onSuccess: () => {
          toast({
            title: "Settings updated",
            variant: "default",
            description: "Your settings have been updated successfully",
          });
          onSave();
        },
      }
    );
  }, [
    updateSettings,
    author,
    repository,
    includePatterns,
    excludePatterns,
    maxFileSize,
    aiPrompt,
    toast,
    onSave,
  ]);

  return (
    <div className="flex-grow overflow-y-auto bg-background">
      <Tabs
        orientation="vertical"
        dir="ltr"
        defaultValue="exclude"
        className="flex min-h-[300px]"
      >
        <TabsList className="flex flex-col h-full space-y-1 bg-background px-2 justify-start">
          <TabItem value="exclude">Exclude</TabItem>
          <TabItem value="include">Include</TabItem>
          <TabItem value="ai">AI</TabItem>
          <TabItem value="advanced">Advanced</TabItem>
        </TabsList>
        <div className="flex-grow px-4">
          <TabsContent value="exclude" className="mt-0">
            <ExcludeTab
              newExcludePattern={newExcludePattern}
              setNewExcludePattern={setNewExcludePattern}
              excludePatterns={excludePatterns}
              onAdd={() => addPattern("exclude")}
              onRemove={removePattern}
              onSave={handleSave}
            />
          </TabsContent>
          <TabsContent value="include" className="mt-0">
            <IncludeTab
              newIncludePattern={newIncludePattern}
              setNewIncludePattern={setNewIncludePattern}
              includePatterns={includePatterns}
              onAdd={() => addPattern("include")}
              onRemove={removePattern}
              onSave={handleSave}
            />
          </TabsContent>
          <TabsContent value="ai" className="mt-0">
            <AITab aiPrompt={aiPrompt} setAiPrompt={setAiPrompt} />
          </TabsContent>
          <TabsContent value="advanced" className="mt-0">
            <AdvancedTab
              maxFileSize={maxFileSize}
              setMaxFileSize={setMaxFileSize}
              onSave={handleSave}
            />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
