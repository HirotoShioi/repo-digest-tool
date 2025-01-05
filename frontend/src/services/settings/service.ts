import client from "@/lib/api/client";
import { components } from "@/lib/api/schema";
import { Settings } from "@/types";

function toSettings(data: components["schemas"]["Settings"]): Settings {
  return {
    includePatterns: data.include_files,
    excludePatterns: data.exclude_files,
    maxTokens: data.max_tokens,
  };
}

type GetSettingsParams = {
  author: string;
  name: string;
};

async function getSettings({ author, name }: GetSettingsParams) {
  const response = await client.GET(
    `/repositories/{author}/{repository_name}/settings`,
    {
      params: {
        path: {
          author,
          repository_name: name,
        },
      },
    }
  );

  if (!response.data) {
    return null;
  }

  return toSettings(response.data);
}

export { getSettings };

export type { GetSettingsParams };