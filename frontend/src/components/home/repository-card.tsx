import { Trash2, RefreshCw, Loader2 } from "lucide-react";
import type { Repository } from "@/types";
import { formatDate } from "@/utils/formatters";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import {
  useDeleteRepository,
  useUpdateRepository,
} from "@/services/repositories/mutations";
import { useToast } from "@/hooks/use-toast";
import { useNavigate } from "@tanstack/react-router";

interface RepositoryCardProps {
  repository: Repository;
}

export function RepositoryCard({ repository }: RepositoryCardProps) {
  const { toast } = useToast();
  const { mutate: deleteRepository, isPending: isDeleting } =
    useDeleteRepository();
  const { mutate: updateRepository, isPending: isUpdating } =
    useUpdateRepository();
  function handleDelete() {
    deleteRepository(
      {
        author: repository.author,
        repositoryName: repository.name,
      },
      {
        onSuccess: () => {
          toast({
            variant: "destructive",
            title: "Repository deleted",
          });
        },
        onError: () => {
          toast({
            variant: "destructive",
            title: "Failed to delete repository",
          });
        },
      }
    );
  }
  function handleUpdate() {
    updateRepository(
      {
        author: repository.author,
        repositoryName: repository.name,
      },
      {
        onSuccess: () => {
          toast({
            variant: "success",
            title: "Repository successfully updated",
          });
        },
        onError: () => {
          toast({
            variant: "destructive",
            title: "Failed to update repository",
          });
        },
      }
    );
  }
  const navigate = useNavigate();

  return (
    <Card
      className={`hover:shadow-lg transition-all cursor-pointer h-full`}
      onClick={() => {
        navigate({
          to: "/$author/$name",
          params: {
            author: repository.author,
            name: repository.name,
          },
        });
      }}
    >
      <CardHeader className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4 max-w-[70%]">
            <div className="flex flex-col w-full">
              <h3 className="text-lg font-semibold">{repository.name}</h3>
              <p className="text-sm text-muted-foreground truncate">
                {repository.url}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleUpdate();
                  }}
                  size="icon"
                  variant="ghost"
                  disabled={isUpdating}
                  data-testid="update-repository-button"
                >
                  {isUpdating ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <RefreshCw className="w-4 h-4" />
                  )}
                </Button>
              </TooltipTrigger>
              <TooltipContent>Update repository</TooltipContent>
            </Tooltip>

            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  disabled={isDeleting}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete();
                  }}
                  size="icon"
                  variant="ghost"
                  className="hover:text-destructive hover:bg-destructive/10"
                  data-testid="delete-repository-button"
                >
                  {isDeleting ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Trash2 className="w-4 h-4" />
                  )}
                </Button>
              </TooltipTrigger>
              <TooltipContent>Delete repository</TooltipContent>
            </Tooltip>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-4 pt-0">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="bg-muted p-3 rounded-md">
            <p className="text-muted-foreground">Branch</p>
            <p className="font-semibold">{repository.branch || "main"}</p>
          </div>
          <div className="bg-muted p-3 rounded-md">
            <p className="text-muted-foreground">Last Updated</p>
            <p className="font-semibold">{formatDate(repository.updatedAt)}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
