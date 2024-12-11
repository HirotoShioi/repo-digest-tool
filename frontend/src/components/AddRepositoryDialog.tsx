import React, { useState } from "react";
import { GitBranch } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useCloneRepository } from "@/services/repositories/mutations";
import { useToast } from "@/hooks/use-toast";
import { LoadingButton } from "@/components/LoadingButton";
interface AddRepositoryDialogProps {
  isOpen: boolean;
  onClose: () => void;
}

export function AddRepositoryDialog({
  isOpen,
  onClose,
}: AddRepositoryDialogProps) {
  const [url, setUrl] = useState("");
  const { toast } = useToast();
  const { mutate: cloneRepository, isPending } = useCloneRepository();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim()) {
      cloneRepository(
        { repositoryIdOrUrl: url.trim() },
        {
          onSuccess: () => {
            setUrl("");
            onClose();
            toast({
              title: "Repository cloned successfully",
              description: "The repository has been added to your list.",
              variant: "success",
            });
          },
        }
      );
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            <div className="flex items-center gap-2">
              <GitBranch className="w-5 h-5" />
              Add New Repository
            </div>
            <DialogDescription>
              Add a new repository to your list.
            </DialogDescription>
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label
              htmlFor="repo-url"
              className="block text-sm font-medium mb-2"
            >
              Repository URL
            </label>
            <Input
              id="repo-url"
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter Git repository URL"
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <LoadingButton
              type="submit"
              isLoading={isPending}
              loadingText="Cloning..."
            >
              Clone Repository
            </LoadingButton>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
