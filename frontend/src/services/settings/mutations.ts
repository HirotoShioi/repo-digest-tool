import client from "@/lib/api/client";
import { useMutation } from "@tanstack/react-query";
import { Settings } from "@/types";
import { useQueryClient } from "@tanstack/react-query";
import { components } from "@/lib/api/schema";

type UpdateSettingsParams = {
  author: string;
  name: string;
  settings: Settings;
};
function useUpdateSettings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (params: UpdateSettingsParams) =>
      client.PUT(`/repositories/{author}/{repository_name}/settings`, {
        params: {
          path: {
            author: params.author!,
            repository_name: params.name!,
          },
        },
        body: {
          include_files: params.settings.includePatterns,
          exclude_files: params.settings.excludePatterns,
          max_tokens: params.settings.maxTokens,
        },
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["settings"] });
    },
  });
}

function toSettings(data: components["schemas"]["Settings"]): Settings {
  return {
    includePatterns: data.include_files,
    excludePatterns: data.exclude_files,
    maxTokens: data.max_tokens,
  };
}

type ExcludeFilesParams = {
  author: string;
  name: string;
  paths: string[];
};

function useExcludeFiles() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (params: ExcludeFilesParams) => {
      let settings = queryClient.getQueryData<Settings>(["settings"]);
      if (!settings) {
        const response = await client.GET(
          "/repositories/{author}/{repository_name}/settings",
          {
            params: {
              path: {
                author: params.author!,
              repository_name: params.name!,
            },
          },
        });
        if (!response.data) {
          throw new Error("Failed to fetch settings");
        }
        settings = toSettings(response.data);
      }
      await client.PUT(
        `/repositories/{author}/{repository_name}/settings`,
        {
          params: {
            path: {
              author: params.author!,
            repository_name: params.name!,
          },
        },
        body: {
          include_files: settings.includePatterns,
          exclude_files: [...settings.excludePatterns, ...params.paths],
          max_tokens: settings.maxTokens,
        },
      });
    },
    onSuccess: (_, params) => {
      queryClient.invalidateQueries({ queryKey: ["settings"] });
      queryClient.invalidateQueries({
        queryKey: ["summary", params.author, params.name],
      });
    },
  });
}

type FilterFilesWithLLMParams = {
  author: string;
  name: string;
  prompt: string;
};

function useFilterFilesWithLLM() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (params: FilterFilesWithLLMParams) => {
      await client.POST(
        `/repositories/{author}/{repository_name}/filter/ai`,
        {
          params: {
            path: {
              author: params.author,
            repository_name: params.name,
          },
        },
        body: {
          prompt: params.prompt,
        },
      });
    },
    onSuccess: (_, params) => {
      queryClient.invalidateQueries({ queryKey: ["settings"] });
      queryClient.invalidateQueries({
        queryKey: ["summary", params.author, params.name],
      });
    },
  });
}

export { useUpdateSettings, useExcludeFiles, useFilterFilesWithLLM };
