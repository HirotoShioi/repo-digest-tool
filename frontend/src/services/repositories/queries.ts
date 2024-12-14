import { useQuery, useQueryClient } from "@tanstack/react-query";
import client from "@/lib/api/client";
import { Repository } from "@/types";
import { components } from "@/lib/api/schema";

type RepositoryResponse = components["schemas"]["Repository"];
function toRepository(r: RepositoryResponse): Repository {
  return {
    id: r.id,
    name: r.name,
    author: r.author,
    path: r.path,
    updatedAt: new Date(r.updated_at),
    branch: r.branch,
    url: r.url,
    size: r.size,
  } satisfies Repository;
}

const useGetRepositories = () => {
  return useQuery<Repository[]>({
    queryKey: ["repositories"],
    queryFn: async () => {
      const response = await client.GET("/repositories");
      return (response.data ?? []).map(toRepository);
    },
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
    queryFn: async () => {
      const response = await client.GET(
        "/repositories/{author}/{repository_name}",
        {
          params: {
            path: {
              author: params.author!,
              repository_name: params.name!,
            },
          },
        }
      );
      if (!response.data) {
        return null;
      }
      return toRepository(response.data);
    },
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
      queryFn: async () => {
        const response = await client.GET(
          "/repositories/{author}/{repository_name}",
          {
            params: {
              path: {
                author: params.author,
                repository_name: params.name,
              },
            },
          }
        );
        return response.data ? toRepository(response.data) : null;
      },
    });
  };
  return prefetch;
};

export { useGetRepositories, useGetRepositoryById, usePrefetchRepositoryById };
