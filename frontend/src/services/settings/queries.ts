import client from "@/lib/api/client";
import { components } from "@/lib/api/schema";
import { Settings } from "@/types";
import { useQuery } from "@tanstack/react-query";

function toSettings(data: components["schemas"]["Settings"]): Settings {
  return {
    includePatterns: data.include_files,
    excludePatterns: data.exclude_files,
    maxFileSize: data.max_file_size,
  };
}

type GetSettingParams = {
  author: string;
  repository: string;
};
function useGetSettings(params: GetSettingParams) {
  return useQuery({
    queryKey: ["settings", params.author, params.repository],
    initialData: {
      includePatterns: [],
      excludePatterns: [],
      maxFileSize: 10,
      aiPrompt: "",
    },
    queryFn: async () => {
      const response = await client.GET("/{author}/{repository_name}/settings", {
        params: {
          path: {
            author: params.author,
            repository_name: params.repository,
          },
        },
      });
      if (!response.data) {
        throw new Error("Failed to fetch settings");
      }
      return toSettings(response.data);
    },
  });
}

export { useGetSettings };
