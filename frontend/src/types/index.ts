export interface Repository {
  id: string;
  name: string;
  url: string;
  lastUpdated: Date;
  size: number;
  fileCount: number;
}

export interface FileStats {
  extension: string;
  count: number;
  totalSize: number;
}

export interface FileFilter {
  extensions: string[];
  minSize?: number;
  maxSize?: number;
  searchQuery: string;
}