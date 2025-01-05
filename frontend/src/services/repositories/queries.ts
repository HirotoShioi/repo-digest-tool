import { queryOptions, useQuery } from "@tanstack/react-query";
import { Repository } from "@/types";
import { getRepositories, getRepositoryById } from "./service";

const useGetRepositories = () => {
  return useQuery<Repository[]>({
    queryKey: ["repositories"],
    queryFn: async () => getRepositories(),
  });
};

type GetRepositoryQueryOptionsParams = {
  author: string;
  name: string;
};

function getRepositoryByIdQueryOptions({
  author,
  name,
}: GetRepositoryQueryOptionsParams) {
  return queryOptions({
    queryKey: ["repository", author, name],
    queryFn: async () => getRepositoryById({ author, name }),
  });
}


export { useGetRepositories, getRepositoryByIdQueryOptions };
