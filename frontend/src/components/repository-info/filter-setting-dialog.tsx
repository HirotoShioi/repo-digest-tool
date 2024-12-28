"use client";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Settings, Ban, Filter, Brain, Wrench } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@radix-ui/react-tabs";
import { MaxTokensTab } from "./max-tokens-tab";
import { AITab } from "./aI-tab";
import { ExcludeTab } from "./exclude-tab";
import { IncludeTab } from "./include-tab";
import {
  FilterSettingsProvider,
  useFilterSettings,
} from "@/contexts/FilterSettingsContext";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";

interface FilterSettingDialogProps {
  onSave: () => void;
  author: string;
  repository: string;
}

function TabItem({
  value,
  children,
  icon: Icon,
}: {
  value: string;
  children: React.ReactNode;
  icon: React.ElementType;
}) {
  return (
    <TabsTrigger
      value={value}
      className="text-left px-3 py-2 hover:bg-muted/80 data-[state=active]:bg-muted w-[140px] rounded-lg transition-all flex items-center gap-2"
    >
      <Icon className="w-4 h-4" />
      {children}
    </TabsTrigger>
  );
}

function DialogContent_({ children }: { children: React.ReactNode }) {
  const { isPending } = useFilterSettings();
  return (
    <DialogContent
      className="p-4 gap-0 max-w-2xl"
      onPointerDownOutside={(e) => {
        if (isPending) {
          e.preventDefault();
        }
      }}
      onEscapeKeyDown={(e) => {
        if (isPending) {
          e.preventDefault();
        }
      }}
    >
      {children}
    </DialogContent>
  );
}

function DialogWrapper({
  open,
  setOpen,
  children,
}: {
  open: boolean;
  setOpen: (open: boolean) => void;
  children: React.ReactNode;
}) {
  const { isPending } = useFilterSettings();
  return (
    <Dialog
      open={open}
      modal={true}
      onOpenChange={(isOpen) => {
        if (!isPending) {
          setOpen(isOpen);
        }
      }}
    >
      {children}
    </Dialog>
  );
}

function FilterSettingDialog({
  onSave,
  author,
  repository,
}: FilterSettingDialogProps) {
  const [open, setOpen] = useState(false);
  const toast = useToast();
  function onClick() {
    toast.dismiss();
    setOpen(true);
  }
  return (
    <FilterSettingsProvider
      author={author}
      repository={repository}
      onSave={onSave}
      setOpen={setOpen}
    >
      <DialogWrapper open={open} setOpen={setOpen}>
        <DialogTrigger asChild>
          <Button
            size="lg"
            className="bg-primary hover:bg-primary/90"
            data-testid="filter-dialog-button"
            onClick={onClick}
          >
            <Settings className="w-4 h-4" />
            Filter
          </Button>
        </DialogTrigger>
        <DialogContent_>
          <DialogHeader className="p-4">
            <DialogTitle className="text-2xl font-semibold">
              Filter Settings
            </DialogTitle>
            <DialogDescription></DialogDescription>
          </DialogHeader>
          <div className="flex-grow overflow-y-auto bg-background">
            <Tabs
              orientation="vertical"
              dir="ltr"
              defaultValue="exclude"
              className="flex min-h-[500px]"
            >
              <TabsList className="flex flex-col h-full space-y-1 bg-background px-2 justify-start">
                <TabItem value="exclude" icon={Ban}>
                  Exclude
                </TabItem>
                <TabItem value="include" icon={Filter}>
                  Include
                </TabItem>
                <TabItem value="ai" icon={Brain}>
                  AI
                </TabItem>
                <TabItem value="max-tokens" icon={Wrench}>
                  Max Tokens
                </TabItem>
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
                <TabsContent value="max-tokens" className="mt-0">
                  <MaxTokensTab />
                </TabsContent>
              </div>
            </Tabs>
          </div>
        </DialogContent_>
      </DialogWrapper>
    </FilterSettingsProvider>
  );
}

export { FilterSettingDialog };
