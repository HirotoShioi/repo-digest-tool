import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { FilterSettingsProvider } from "@/contexts/FilterSettingsContext";
import { ExcludeTab } from "./tabs/ExcludeTab";
import { IncludeTab } from "./tabs/IncludeTab";
import { AITab } from "./tabs/AITab";
import { AdvancedTab } from "./tabs/AdvancedTab";

interface FilterTabsProps {
  onSave: () => void;
  author: string;
  repository: string;
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

function FilterTabsContent() {
  return (
    <div className="flex-grow overflow-y-auto bg-background">
      <Tabs
        orientation="vertical"
        dir="ltr"
        defaultValue="exclude"
        className="flex min-h-[500px]"
      >
        <TabsList className="flex flex-col h-full space-y-1 bg-background px-2 justify-start">
          <TabItem value="exclude">Exclude</TabItem>
          <TabItem value="include">Include</TabItem>
          <TabItem value="ai">AI</TabItem>
          <TabItem value="advanced">Advanced</TabItem>
        </TabsList>
        <div className="flex-grow px-4">
          <TabsContent value="exclude" className="mt-0">
            <ExcludeTab />
          </TabsContent>
          <TabsContent value="include" className="mt-0">
            <IncludeTab />
          </TabsContent>
          <TabsContent value="ai" className="mt-0">
            <AITab />
          </TabsContent>
          <TabsContent value="advanced" className="mt-0">
            <AdvancedTab />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}

export function FilterTabs({ author, repository, onSave }: FilterTabsProps) {
  return (
    <FilterSettingsProvider
      author={author}
      repository={repository}
      onSave={onSave}
    >
      <FilterTabsContent />
    </FilterSettingsProvider>
  );
}
