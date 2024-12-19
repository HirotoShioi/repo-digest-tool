import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

function FilterTabs() {
  return (
    <div className="flex-grow overflow-y-auto bg-background">
      <Tabs
        orientation="vertical"
        dir="ltr"
        defaultValue="exclude"
        className="flex min-h-[300px] h-full"
      >
        <TabsList className="flex flex-col h-full w-[200px] space-y-1 bg-background px-2 justify-start">
          <TabsTrigger
            value="exclude"
            className="justify-start w-full px-3 py-2 hover:bg-muted/80 data-[state=active]:bg-muted"
          >
            Exclude
          </TabsTrigger>
          <TabsTrigger
            value="include"
            className="justify-start w-full px-3 py-2 hover:bg-muted/80 data-[state=active]:bg-muted"
          >
            Include
          </TabsTrigger>
          <TabsTrigger
            value="ai"
            className="justify-start w-full px-3 py-2 hover:bg-muted/80 data-[state=active]:bg-muted"
          >
            AI
          </TabsTrigger>
          <TabsTrigger
            value="advanced"
            className="justify-start w-full px-3 py-2 hover:bg-muted/80 data-[state=active]:bg-muted"
          >
            Advanced
          </TabsTrigger>
        </TabsList>
        <div className="flex-grow p-6">
          <TabsContent value="exclude" className="mt-0">
            Exclude content
          </TabsContent>
          <TabsContent value="include" className="mt-0">
            Include content
          </TabsContent>
          <TabsContent value="ai" className="mt-0">
            AI content
          </TabsContent>
          <TabsContent value="advanced" className="mt-0">
            Advanced content
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}

export default FilterTabs;
