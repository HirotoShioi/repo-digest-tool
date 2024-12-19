import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
} from "react";
import { useGetSettings } from "@/services/settings/queries";
import { useUpdateSettings } from "@/services/settings/mutations";
import { useToast } from "@/hooks/use-toast";
import { Minimatch } from "minimatch";

interface FilterSettingsContextType {
  excludePatterns: string[];
  includePatterns: string[];
  maxFileSize: number;
  newExcludePattern: string;
  newIncludePattern: string;
  setNewExcludePattern: (pattern: string) => void;
  setNewIncludePattern: (pattern: string) => void;
  setExcludePatterns: (patterns: string[]) => void;
  setIncludePatterns: (patterns: string[]) => void;
  setMaxFileSize: (size: number) => void;
  addPattern: (type: "exclude" | "include") => void;
  removePattern: (pattern: string, type: "exclude" | "include") => void;
  handleSave: () => void;
  onSave: () => void;
}

const FilterSettingsContext = createContext<
  FilterSettingsContextType | undefined
>(undefined);

function isValidGlob(pattern: string): boolean {
  if (!pattern || pattern.trim().length === 0) return false;

  try {
    new Minimatch(pattern);
    return true;
  } catch {
    return false;
  }
}

interface FilterSettingsProviderProps {
  children: React.ReactNode;
  author: string;
  repository: string;
  onSave: () => void;
}

export function FilterSettingsProvider({
  children,
  author,
  repository,
  onSave,
}: FilterSettingsProviderProps) {
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

  // Initialize state from filterSettings
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

  const value = {
    excludePatterns,
    includePatterns,
    maxFileSize,
    newExcludePattern,
    newIncludePattern,
    setNewExcludePattern,
    setNewIncludePattern,
    setExcludePatterns,
    setIncludePatterns,
    setMaxFileSize,
    addPattern,
    removePattern,
    handleSave,
    onSave,
  };

  return (
    <FilterSettingsContext.Provider value={value}>
      {children}
    </FilterSettingsContext.Provider>
  );
}

export function useFilterSettings() {
  const context = useContext(FilterSettingsContext);
  if (context === undefined) {
    throw new Error(
      "useFilterSettings must be used within a FilterSettingsProvider"
    );
  }
  return context;
}
