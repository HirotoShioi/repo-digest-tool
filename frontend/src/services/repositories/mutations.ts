import { useMutation, useQueryClient } from "@tanstack/react-query";
import client from "@/lib/api/client";
import { extractAuthorAndNameFromUrl } from "@/lib/utils";

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
  repositoryIdOrUrl: string;
};

const useDeleteRepository = () => {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: (params: DeleteRepositoryParams) => {
      return client.DELETE("/repositories", {
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

type UpdateRepositoryParams = {
  repositoryIdOrUrl?: string;
};

const useUpdateRepository = () => {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: (params: UpdateRepositoryParams) => {
      return client.PUT("/repositories", {
        body: {
          url: params.repositoryIdOrUrl,
        },
      });
    },
    onSuccess: (_, params: UpdateRepositoryParams) => {
      queryClient.invalidateQueries({ queryKey: ["repositories"] });
      const { author, name } = extractAuthorAndNameFromUrl(
        params.repositoryIdOrUrl!
      ) ?? {};
      if (author && name) {
        queryClient.invalidateQueries({ queryKey: ["summary", author, name] });
      }
    },
  });

  return mutation;
};

export { useCloneRepository, useDeleteRepository, useUpdateRepository };
