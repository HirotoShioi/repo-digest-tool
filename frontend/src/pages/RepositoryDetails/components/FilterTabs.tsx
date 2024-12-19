import { useState, useCallback, useEffect, memo } from "react";
import { Plus, X } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { useGetSettings } from "@/services/settings/queries";
import { useUpdateSettings } from "@/services/settings/mutations";
import { useToast } from "@/hooks/use-toast";
import { Minimatch } from "minimatch";

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

const PatternInput = memo(function PatternInput({
  value,
  onChange,
  onAdd,
  placeholder,
}: {
  value: string;
  onChange: (value: string) => void;
  onAdd: () => void;
  placeholder: string;
}) {
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
});

const PatternList = memo(function PatternList({
  patterns,
  type,
  onRemove,
}: {
  patterns: string[];
  type: "exclude" | "include";
  onRemove: (pattern: string, type: "exclude" | "include") => void;
}) {
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
});

function FilterTabs({ author, repository, onSave }: FilterTabsProps) {
  const { data: filterSettings } = useGetSettings({
    author,
    repository,
  });
  const { toast } = useToast();
  const { mutate: updateSettings } = useUpdateSettings();

  const [excludePatterns, setExcludePatterns] = useState<string[]>([]);
  const [includePatterns, setIncludePatterns] = useState<string[]>([]);
  const [maxFileSize, setMaxFileSize] = useState<number>(10);
  const [newExcludePattern, setNewExcludePattern] = useState("");
  const [newIncludePattern, setNewIncludePattern] = useState("");

  useEffect(() => {
    if (filterSettings) {
      setExcludePatterns(filterSettings.excludePatterns || []);
      setIncludePatterns(filterSettings.includePatterns || []);
      setMaxFileSize(filterSettings.maxFileSize || 10);
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
          <TabsTrigger
            value="exclude"
            className="justify-start w-full px-3 py-2 hover:bg-muted/80 data-[state=active]:bg-muted w-[120px]"
          >
            Exclude
          </TabsTrigger>
          <TabsTrigger
            value="include"
            className="justify-start w-full px-3 py-2 hover:bg-muted/80 data-[state=active]:bg-muted w-[120px]"
          >
            Include
          </TabsTrigger>
          <TabsTrigger
            value="advanced"
            className="justify-start w-full px-3 py-2 hover:bg-muted/80 data-[state=active]:bg-muted w-[120px]"
          >
            Advanced
          </TabsTrigger>
        </TabsList>
        <div className="flex-grow px-4">
          <TabsContent value="exclude" className="mt-0 space-y-4">
            <div>
              <h3 className="font-medium">Exclude Patterns</h3>
              <p className="text-sm text-muted-foreground">
                Specify patterns for files and directories to exclude from
                processing
              </p>
            </div>
            <PatternInput
              value={newExcludePattern}
              onChange={setNewExcludePattern}
              onAdd={() => addPattern("exclude")}
              placeholder="Add new exclude pattern (e.g. *.log)"
            />
            <PatternList
              patterns={excludePatterns}
              type="exclude"
              onRemove={removePattern}
            />
          </TabsContent>
          <TabsContent value="include" className="mt-0 space-y-4">
            <div>
              <h3 className="font-medium">Include Patterns</h3>
              <p className="text-sm text-muted-foreground">
                Specify patterns for files that should always be included
              </p>
            </div>
            <PatternInput
              value={newIncludePattern}
              onChange={setNewIncludePattern}
              onAdd={() => addPattern("include")}
              placeholder="Add new include pattern (e.g. *.md)"
            />
            <PatternList
              patterns={includePatterns}
              type="include"
              onRemove={removePattern}
            />
          </TabsContent>
          <TabsContent value="advanced" className="mt-0 space-y-4">
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
          </TabsContent>
        </div>
      </Tabs>
      <div className="flex justify-end mt-4 px-4">
        <Button onClick={handleSave}>Save Settings</Button>
      </div>
    </div>
  );
}

export default FilterTabs;
