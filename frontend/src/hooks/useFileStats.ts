import { useState } from 'react';
import type { FileStats, FileFilter } from '../types';

export function useFileStats(author: string, name: string) {
  const [fileStats] = useState<FileStats[]>([
    { extension: '.js', count: 25, totalSize: 156000 },
    { extension: '.ts', count: 15, totalSize: 89000 },
    { extension: '.json', count: 5, totalSize: 12000 },
    { extension: '.md', count: 3, totalSize: 8000 }
  ]);

  const generateDigest = (filter: FileFilter) => {
    console.log('Generating digest for repository:', author, name, 'with filter:', filter);
  };

  return {
    fileStats,
    generateDigest
  };
}