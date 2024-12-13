import client from "@/lib/api/client";
import { useMutation } from "@tanstack/react-query";
import { Settings } from "@/types";
import { useQueryClient } from "@tanstack/react-query";
import { components } from "@/lib/api/schema";

function useUpdateSettings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (settings: Settings) =>
      client.PUT("/settings", {
        body: {
          include_files: settings.includePatterns,
          exclude_files: settings.excludePatterns,
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
        const response = await client.GET("/settings");
        if (!response.data) {
          throw new Error("Failed to fetch settings");
        }
        settings = toSettings(response.data);
      }
      await client.PUT("/settings", {
        body: {
          include_files: settings.includePatterns,
          exclude_files: [...settings.excludePatterns, ...params.paths],
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
