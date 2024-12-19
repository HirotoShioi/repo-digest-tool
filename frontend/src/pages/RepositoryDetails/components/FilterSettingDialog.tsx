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
import FilterTabs from "./FilterTabs";
import { Settings } from "lucide-react";

interface FilterSettingDialogProps {
  onSave: () => void;
  author: string;
  repository: string;
}
function FilterSettingDialog({
  onSave,
  author,
  repository,
}: FilterSettingDialogProps) {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button
          size="lg"
          className="bg-primary hover:bg-primary/90"
          data-testid="filter-dialog-button"
        >
          <Settings className="w-4 h-4" />
          Filter
        </Button>
      </DialogTrigger>
      <DialogContent className="p-4 gap-0 max-w-2xl">
        <DialogHeader className="p-4">
          <DialogTitle className="text-2xl font-semibold">
            Filter Settings
          </DialogTitle>
          <DialogDescription></DialogDescription>
        </DialogHeader>
        <FilterTabs onSave={onSave} author={author} repository={repository} />
      </DialogContent>
    </Dialog>
  );
}

export { FilterSettingDialog };
