import { useMutation, useQueryClient } from "@tanstack/react-query";
import client from "@/lib/api/client";

type CloneRepositoryParams = {
  repositoryIdOrUrl: string;
};

const useCloneRepository = () => {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: (params: CloneRepositoryParams) => {
      return client.POST("/repositories", {
        body: {
          url: params.repositoryIdOrUrl,
        },
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["repositories"] });
    },
  });

  return mutation;
};

type DeleteRepositoryParams = {
  author: string;
  repositoryName: string;
};

const useDeleteRepository = () => {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: (params: DeleteRepositoryParams) => {
      return client.DELETE(
        "/repositories/{author}/{repository_name}",
        {
          params: {
            path: {
              author: params.author,
              repository_name: params.repositoryName,
            },
          },
        }
      );
    },
    onSuccess: (_, params: DeleteRepositoryParams) => {
      queryClient.invalidateQueries({ queryKey: ["repositories"] });
      queryClient.invalidateQueries({
        queryKey: ["summary", params.author, params.repositoryName],
      });
    },
  });

  return mutation;
};

type UpdateRepositoryParams = {
  author: string;
  repositoryName: string;
};

const useUpdateRepository = () => {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: (params: UpdateRepositoryParams) => {
      return client.PUT("/repositories/{author}/{repository_name}", {
        params: {
          path: {
            author: params.author,
            repository_name: params.repositoryName,
          },
        },
      });
    },
    onSuccess: (_, params: UpdateRepositoryParams) => {
      queryClient.invalidateQueries({ queryKey: ["repositories"] });
      queryClient.invalidateQueries({
        queryKey: ["summary", params.author, params.repositoryName],
      });
    },
  });

  return mutation;
};

export { useCloneRepository, useDeleteRepository, useUpdateRepository };
