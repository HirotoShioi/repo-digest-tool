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

export type { Repository, FileStats, FileFilter };