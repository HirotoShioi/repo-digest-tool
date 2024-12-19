type Repository = {
  id: string;
  name: string;
  author: string;
  path: string;
  updatedAt: Date;
  branch: string | null;
  url: string;
  size: number;
}


type FileStats = {
  extension: string;
  count: number;
  totalSize: number;
}

type FileFilter = {
  extensions: string[];
  minSize?: number;
  maxSize?: number;
  searchQuery: string;
}

type FileTypeAggregation = {
  extension: string;
  count: number;
  tokens: number;
}

type FileData = {
  name: string;
  path: string;
  extension: string;
  tokens: number;
}

type Summary = {
  repository: string;
  totalFiles: number;
  totalSizeKb: number;
  averageFileSizeKb: number;
  maxFileSizeKb: number;
  minFileSizeKb: number;
  fileTypes: FileTypeAggregation[];
  contextLength: number;
  fileData: FileData[];
}

type Settings = {
  includePatterns: string[];
  excludePatterns: string[];
  maxFileSize: number;
  aiPrompt?: string;
}

export type { Repository, FileStats, FileFilter, Summary, FileTypeAggregation, FileData, Settings };
