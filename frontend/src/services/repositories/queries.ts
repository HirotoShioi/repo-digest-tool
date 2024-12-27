import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Repository } from "@/types";
import { getRepositories, getRepositoryById } from "./service";

const useGetRepositories = () => {
  return useQuery<Repository[]>({
    queryKey: ["repositories"],
    queryFn: async () => getRepositories(),
  });
};

type GetRepositoryByIdParams = {
  author?: string;
  name?: string;
};

const useGetRepositoryById = (params: GetRepositoryByIdParams) => {
  return useQuery<Repository | null>({
    queryKey: ["repository", params.author, params.name],
    enabled: !!params.author && !!params.name,
    queryFn: async () =>
      getRepositoryById({
        author: params.author!,
        name: params.name!,
      }),
  });
};

type PrefetchRepositoryByIdParams = {
  author: string;
  name: string;
};
const usePrefetchRepositoryById = (params: PrefetchRepositoryByIdParams) => {
  const queryClient = useQueryClient();
  const prefetch = () => {
    queryClient.prefetchQuery({
      queryKey: ["repository", params.author, params.name],
      staleTime: 1000 * 60 * 5, // 5 minutes
      queryFn: async () => getRepositoryById(params),
    });
  };
  return prefetch;
};

export { useGetRepositories, useGetRepositoryById, usePrefetchRepositoryById };
