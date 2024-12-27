import React, { useState } from "react";
import { GitBranch, PlusCircle } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useCloneRepository } from "@/services/repositories/mutations";
import { useToast } from "@/hooks/use-toast";
import { LoadingButton } from "@/components/loading-button";

export function AddRepositoryDialog() {
  const [open, setOpen] = useState(false);
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
            setOpen(false);
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
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <PlusCircle className="w-5 h-5" />
          Add Repository
        </Button>
      </DialogTrigger>
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
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
            >
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
