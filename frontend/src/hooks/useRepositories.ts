import { useState } from 'react';
import type { Repository } from '../types';

export function useRepositories() {
  const [repositories, setRepositories] = useState<Repository[]>([]);

  const addRepository = (url: string) => {
    const newRepo: Repository = {
      id: Date.now().toString(),
      name: url.split('/').pop()?.replace('.git', '') || 'Unknown',
      url,
      lastUpdated: new Date(),
      size: 265000,
      fileCount: 48
    };
    setRepositories([...repositories, newRepo]);
  };

  const deleteRepository = (id: string) => {
    setRepositories(repositories.filter(repo => repo.id !== id));
  };

  const updateRepository = (id: string) => {
    // Implement repository update logic
    console.log('Updating repository:', id);
  };

  const getRepository = (id: string | undefined) => {
    return repositories.find(repo => repo.id === id);
  };

  return {
    repositories,
    addRepository,
    deleteRepository,
    updateRepository,
    getRepository
  };
}