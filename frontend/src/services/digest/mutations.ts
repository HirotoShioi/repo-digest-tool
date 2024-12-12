import { useMutation } from "@tanstack/react-query";

interface GenerateDigestParams {
  author: string;
  repositoryName: string;
}

export const useGenerateDigest = () => {
  return useMutation({
    mutationFn: async (params: GenerateDigestParams) => {
      // なぜかopenapi fetchではダウンロードできない
      const response = await fetch(`http://localhost:8000/digest`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: `https://github.com/${params.author}/${params.repositoryName}`,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to generate digest");
      }

      // Get the blob from response
      const blob = await response.blob();
      // Create download URL
      const downloadUrl = window.URL.createObjectURL(blob);

      // Trigger download
      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = getDefaultFilename(params.author, params.repositoryName);
      document.body.appendChild(link);
      link.click();

      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);

      return { success: true };
    },
  });
};

const getDefaultFilename = (author: string, repositoryName: string): string => {
  const repoName = repositoryName;
  return `${author}_${repoName}_digest.txt`;
};
