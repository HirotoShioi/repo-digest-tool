import { queryOptions, useQuery } from "@tanstack/react-query";
import { getSettings } from "./service";  

type GetSettingParams = {
  author: string;
  name: string;
};

function getSettingsQueryOptions({
  author,
  name,
}: GetSettingParams) {
  return queryOptions({
    queryKey: ["settings", author, name],
    queryFn: async () => getSettings({ author, name }),
  });
}

function useGetSettings(params: GetSettingParams) {
  return useQuery(getSettingsQueryOptions(params));
}

export { useGetSettings, getSettingsQueryOptions };
