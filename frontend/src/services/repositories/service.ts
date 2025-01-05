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

async function getRepositories(): Promise<Repository[]> {
  const response = await client.GET("/repositories");
  return (response.data ?? []).map(toRepository);
}

type GetRepositoryByIdParams = {
  author: string;
  name: string;
};

async function getRepositoryById(
  params: GetRepositoryByIdParams
): Promise<Repository | null> {
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
}

export { getRepositoryById, getRepositories };

export type { GetRepositoryByIdParams };