import { createContext, useContext, useCallback } from "react";
import { useGetSettings } from "@/services/settings/queries";
import {
  useFilterFilesWithLLM,
  useUpdateSettings,
} from "@/services/settings/mutations";
import { useToast } from "@/hooks/use-toast";

interface SavePatternSettings {
  includePatterns: string[];
  excludePatterns: string[];
}

interface SaveSizeSettings {
  maxTokens: number;
}

interface FilterSettingsContextType {
  initialSettings: {
    includePatterns: string[];
    excludePatterns: string[];
    maxTokens: number;
  } | null;
  handleSavePatterns: (settings: SavePatternSettings) => void;
  handleSaveSize: (settings: SaveSizeSettings) => void;
  onSave: () => void;
  author: string;
  repository: string;
  closeDialog: () => void;
  onFilterFilesWithLLM: (prompt: string) => void;
  isPending: boolean;
}

const FilterSettingsContext = createContext<
  FilterSettingsContextType | undefined
>(undefined);

interface FilterSettingsProviderProps {
  children: React.ReactNode;
  author: string;
  repository: string;
  onSave: () => void;
  setOpen: (open: boolean) => void;
}

export function FilterSettingsProvider({
  children,
  author,
  repository,
  onSave,
  setOpen,
}: FilterSettingsProviderProps) {
  const { data: filterSettings } = useGetSettings({
    author,
    repository,
  });
  const { toast } = useToast();
  const { mutate: updateSettings } = useUpdateSettings();

  const handleSavePatterns = useCallback(
    (settings: SavePatternSettings) => {
      updateSettings(
        {
          author,
          name: repository,
          settings: {
            ...settings,
            maxTokens: filterSettings?.maxTokens || 10,
          },
        },
        {
          onSuccess: () => {
            toast({
              title: "Settings updated",
              variant: "default",
              description:
                "Your pattern settings have been updated successfully",
            });
            onSave();
          },
        }
      );
    },
    [
      updateSettings,
      author,
      repository,
      filterSettings?.maxTokens,
      toast,
      onSave,
    ]
  );

  const handleSaveSize = useCallback(
    (settings: SaveSizeSettings) => {
      updateSettings(
        {
          author,
          name: repository,
          settings: {
            includePatterns: filterSettings?.includePatterns || [],
            excludePatterns: filterSettings?.excludePatterns || [],
            ...settings,
          },
        },
        {
          onSuccess: () => {
            toast({
              title: "Settings updated",
              variant: "default",
              description: "Your size settings have been updated successfully",
            });
            onSave();
          },
        }
      );
    },
    [
      updateSettings,
      author,
      repository,
      filterSettings?.includePatterns,
      filterSettings?.excludePatterns,
      toast,
      onSave,
    ]
  );
  const { mutate, isPending } = useFilterFilesWithLLM();

  function onFilterFilesWithLLM(prompt: string) {
    mutate(
      {
        prompt,
        author,
        name: repository,
      },
      { onSuccess: () => onSave() }
    );
  }

  const value = {
    initialSettings: filterSettings,
    handleSavePatterns,
    handleSaveSize,
    onSave,
    author,
    repository,
    closeDialog: () => setOpen(false),
    onFilterFilesWithLLM,
    isPending,
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
