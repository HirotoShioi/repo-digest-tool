import { useQuery, useQueryClient } from "@tanstack/react-query";
import client from "@/lib/api/client";
import { Repository } from "@/types";
import { components } from "@/lib/api/schema";
import { useState } from "react";

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
    initialData: [],
    queryFn: async () => {
      const response = await client.GET("/repositories");
      return (response.data ?? []).map(toRepository);
    },
  });
};

type GetRepositoryByIdParams = {
  author: string;
  name: string;
};

const useGetRepositoryById = (params: GetRepositoryByIdParams) => {
  return useQuery<Repository | null>({
    queryKey: ["repository", params.author, params.name],
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
      if (!response.data) {
        return null;
      }
      return toRepository(response.data);
    },
  });
};

const usePrefetchRepositoryById = (params: GetRepositoryByIdParams) => {
  const queryClient = useQueryClient();
  const [isPrefetched, setIsPrefetched] = useState(false);
  const prefetch = () => {
    if (isPrefetched) {
      return;
    }
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
        setIsPrefetched(true);
        return response.data ? toRepository(response.data) : null;
      },
    });
  };
  return prefetch;
};

export { useGetRepositories, useGetRepositoryById, usePrefetchRepositoryById };
