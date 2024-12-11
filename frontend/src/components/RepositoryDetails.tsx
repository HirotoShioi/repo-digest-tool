import React, { useState } from "react";
import { FileText, Download, Filter } from "lucide-react";
import type { Repository, FileStats, FileFilter } from "../types";

interface RepositoryDetailsProps {
  repository: Repository;
  fileStats: FileStats[];
  onGenerateDigest: (filter: FileFilter) => void;
}

export function RepositoryDetails({
  repository,
  fileStats,
  onGenerateDigest,
}: RepositoryDetailsProps) {
  const [filter, setFilter] = useState<FileFilter>({
    extensions: [],
    searchQuery: "",
  });

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <FileText className="w-5 h-5 text-blue-600" />
          Repository Details
        </h2>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {fileStats.map((stat) => (
            <div key={stat.extension} className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-500">
                Files with {stat.extension || "no extension"}
              </p>
              <p className="text-lg font-semibold">{stat.count}</p>
              <p className="text-sm text-gray-600">
                {formatSize(stat.totalSize)}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Filter className="w-5 h-5 text-blue-600" />
            Filter Files
          </h3>
          <button
            onClick={() => onGenerateDigest(filter)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            <Download className="w-4 h-4" />
            Generate Digest
          </button>
        </div>

        <div className="space-y-4">
          <input
            type="text"
            value={filter.searchQuery}
            onChange={(e) =>
              setFilter({ ...filter, searchQuery: e.target.value })
            }
            placeholder="Search files..."
            className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />

          <div className="flex flex-wrap gap-2">
            {fileStats.map((stat) => (
              <label
                key={stat.extension}
                className="flex items-center space-x-2"
              >
                <input
                  type="checkbox"
                  checked={filter.extensions.includes(stat.extension)}
                  onChange={(e) => {
                    const extensions = e.target.checked
                      ? [...filter.extensions, stat.extension]
                      : filter.extensions.filter(
                          (ext) => ext !== stat.extension
                        );
                    setFilter({ ...filter, extensions });
                  }}
                  className="rounded text-blue-600 focus:ring-blue-500"
                />
                <span>{stat.extension || "no extension"}</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function formatSize(bytes: number): string {
  const units = ["B", "KB", "MB", "GB"];
  let size = bytes;
  let unitIndex = 0;

  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }

  return `${size.toFixed(1)} ${units[unitIndex]}`;
}
