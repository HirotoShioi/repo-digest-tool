import client from "@/lib/api/client";
import { components } from "@/lib/api/schema";
import { Summary } from "@/types";
import { useQuery } from "@tanstack/react-query";

function toSummary(response: components["schemas"]["Summary"]): Summary {
  return {
    repository: response.repository,
    totalFiles: response.total_files,
    totalSizeKb: response.total_size_kb,
    averageFileSizeKb: response.average_file_size_kb,
    maxFileSizeKb: response.max_file_size_kb,
    minFileSizeKb: response.min_file_size_kb,
    fileTypes: response.file_types.map(
      (fileType: components["schemas"]["FileType"]) => ({
        extension: fileType.extension,
        count: fileType.count,
        tokens: fileType.tokens,
      })
    ),
    contextLength: response.context_length,
    fileData: response.file_data.map(
      (file: components["schemas"]["FileData"]) => ({
        name: file.name,
        path: file.path,
        extension: file.extension,
        tokens: file.tokens,
      })
    ),
  };
}

type GetSummaryParams = { author?: string; name?: string };
function useGetSummary(params: GetSummaryParams) {
  const query = useQuery({
    queryKey: ["summary", params.author, params.name],
    enabled: !!params.author && !!params.name,
    queryFn: async () => {
      console.log("useGetSummary");
      const response = await client.GET("/summary/{author}/{repository_name}", {
        params: {
          path: {
            author: params.author!,
            repository_name: params.name!,
          },
        },
      });
      console.log(response);
      return response?.data ? toSummary(response.data) : null;
    },
  });
  return query;
}

export { useGetSummary };
