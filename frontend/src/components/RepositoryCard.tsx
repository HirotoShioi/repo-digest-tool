import {
  Trash2,
  RefreshCw,
  FolderGit2,
  ChevronRight,
  Loader2,
} from "lucide-react";
import type { Repository } from "../types";
import { formatSize, formatDate } from "../utils/formatters";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader } from "./ui/card";
import { Tooltip, TooltipContent, TooltipTrigger } from "./ui/tooltip";
import {
  useDeleteRepository,
  useUpdateRepository,
} from "@/services/repositories/mutations";

interface RepositoryCardProps {
  repository: Repository;
  onSelect: (repository: Repository) => void;
  isSelected: boolean;
}

export function RepositoryCard({
  repository,
  onSelect,
  isSelected,
}: RepositoryCardProps) {
  const { mutate: deleteRepository } = useDeleteRepository();
  const { mutate: updateRepository, isPending: isUpdating } =
    useUpdateRepository();
  function handleDelete() {
    deleteRepository({ repositoryIdOrUrl: repository.url });
  }
  function handleUpdate() {
    updateRepository({ repositoryIdOrUrl: repository.url });
  }
  return (
    <Card
      onClick={() => onSelect(repository)}
      className={`hover:shadow-lg transition-all cursor-pointer
        ${isSelected ? "ring-2 ring-primary" : ""}`}
    >
      <CardHeader className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <FolderGit2 className="w-6 h-6 text-primary" />
            <div>
              <h3 className="text-lg font-semibold">{repository.name}</h3>
              <p className="text-sm text-muted-foreground">{repository.url}</p>
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
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete();
                  }}
                  size="icon"
                  variant="ghost"
                  className="hover:text-destructive hover:bg-destructive/10"
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>Delete repository</TooltipContent>
            </Tooltip>

            <ChevronRight
              className={`w-5 h-5 transition-transform ${
                isSelected ? "rotate-90" : ""
              }`}
            />
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-4 pt-0">
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div className="bg-muted p-3 rounded-md">
            <p className="text-muted-foreground">Author</p>
            <p className="font-semibold">{repository.author}</p>
          </div>
          <div className="bg-muted p-3 rounded-md">
            <p className="text-muted-foreground">Size</p>
            <p className="font-semibold">{formatSize(repository.size)}</p>
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
