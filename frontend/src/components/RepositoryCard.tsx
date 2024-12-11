import React from "react";
import { Trash2, RefreshCw, FolderGit2, ChevronRight } from "lucide-react";
import type { Repository } from "../types";
import { formatSize, formatDate } from "../utils/formatters";

interface RepositoryCardProps {
  repository: Repository;
  onDelete: (id: string) => void;
  onUpdate: (id: string) => void;
  onSelect: (repository: Repository) => void;
  isSelected: boolean;
}

export function RepositoryCard({
  repository,
  onDelete,
  onUpdate,
  onSelect,
  isSelected,
}: RepositoryCardProps) {
  return (
    <div
      onClick={() => onSelect(repository)}
      className={`bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-all cursor-pointer
        ${isSelected ? "ring-2 ring-blue-500" : ""}`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <FolderGit2 className="w-6 h-6 text-blue-600" />
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {repository.name}
            </h3>
            <p className="text-sm text-gray-500">{repository.url}</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={(e) => {
              e.stopPropagation();
              onUpdate(repository.id);
            }}
            className="p-2 text-gray-600 hover:text-blue-600 rounded-full hover:bg-blue-50 transition-colors"
            title="Update repository"
          >
            <RefreshCw className="w-5 h-5" />
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onDelete(repository.id);
            }}
            className="p-2 text-gray-600 hover:text-red-600 rounded-full hover:bg-red-50 transition-colors"
            title="Delete repository"
          >
            <Trash2 className="w-5 h-5" />
          </button>
          <ChevronRight
            className={`w-5 h-5 transition-transform ${
              isSelected ? "rotate-90" : ""
            }`}
          />
        </div>
      </div>
      <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
        <div className="bg-gray-50 p-3 rounded-md">
          <p className="text-gray-500">Files</p>
          <p className="font-semibold">{repository.fileCount}</p>
        </div>
        <div className="bg-gray-50 p-3 rounded-md">
          <p className="text-gray-500">Size</p>
          <p className="font-semibold">{formatSize(repository.size)}</p>
        </div>
        <div className="bg-gray-50 p-3 rounded-md">
          <p className="text-gray-500">Last Updated</p>
          <p className="font-semibold">{formatDate(repository.lastUpdated)}</p>
        </div>
      </div>
    </div>
  );
}
