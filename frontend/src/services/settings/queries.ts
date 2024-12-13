import client from "@/lib/api/client";
import { components } from "@/lib/api/schema";
import { Settings } from "@/types";
import { useQuery } from "@tanstack/react-query";

function toSettings(data: components["schemas"]["Settings"]): Settings {
  return {
    includePatterns: data.include_files,
    excludePatterns: data.exclude_files,
  };
}

function useGetSettings() {
  return useQuery({
    queryKey: ["settings"],
    initialData: {
      includePatterns: [],
      excludePatterns: [],
    },
    queryFn: async () => {
      const response = await client.GET("/settings");
      if (!response.data) {
        throw new Error("Failed to fetch settings");
      }
      return toSettings(response.data);
    },
  });
}

export { useGetSettings };
