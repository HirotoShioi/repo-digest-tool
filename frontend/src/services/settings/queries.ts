import { useQuery } from "@tanstack/react-query";
import { getSettings } from "./service";  

type GetSettingParams = {
  author: string;
  name: string;
};
function useGetSettings(params: GetSettingParams) {
  return useQuery({
    queryKey: ["settings", params.author, params.name],
    initialData: {
      includePatterns: [],
      excludePatterns: [],
      maxTokens: 10,
    },
    queryFn: () => getSettings(params),
  });
}

export { useGetSettings };
