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
      client.PUT(`/{author}/{repository_name}/settings`, {
        params: {
          path: {
            author: params.author!,
            repository_name: params.name!,
          },
        },
        body: {
          include_files: params.settings.includePatterns,
          exclude_files: params.settings.excludePatterns,
          max_file_size: params.settings.maxFileSize,
          ai_prompt: params.settings.aiPrompt,
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
    maxFileSize: data.max_file_size,
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
        const response = await client.GET("/{author}/{repository_name}/settings", {
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
      await client.PUT(`/{author}/{repository_name}/settings`, {
        params: {
          path: {
            author: params.author!,
            repository_name: params.name!,
          },
        },
        body: {
          include_files: settings.includePatterns,
          exclude_files: [...settings.excludePatterns, ...params.paths],
          max_file_size: settings.maxFileSize,
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

export { useUpdateSettings, useExcludeFiles };
