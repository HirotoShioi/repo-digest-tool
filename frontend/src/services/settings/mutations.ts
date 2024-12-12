import client from "@/lib/api/client";
import { useMutation } from "@tanstack/react-query";
import { Settings } from "@/types";
import { useQueryClient } from "@tanstack/react-query";

function useUpdateSettings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (settings: Settings) => client.PUT("/settings", {
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

export { useUpdateSettings };