import client from "@/lib/api/client";
import { useMutation } from "@tanstack/react-query";
import { Settings } from "@/types";
function useUpdateSettings() {
  return useMutation({
    mutationFn: (settings: Settings) => client.PUT("/settings", {
        body: {
            include_files: settings.includePatterns,
            exclude_files: settings.excludePatterns,
        },
    }),
  });
}

export { useUpdateSettings };