import { useParams, useNavigate } from "react-router";
import { ArrowLeft } from "lucide-react";
import { RepositoryDetails } from "@/components/RepositoryDetails";
import { useRepositories } from "@/hooks/useRepositories";
import { useFileStats } from "@/hooks/useFileStats";

export function RepositoryDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { getRepository } = useRepositories();
  const { fileStats, generateDigest } = useFileStats(id);

  const repository = getRepository(id);

  if (!repository) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Repository not found</p>
        <button
          onClick={() => navigate("/")}
          className="mt-4 text-blue-600 hover:text-blue-800"
        >
          Return to repository list
        </button>
      </div>
    );
  }

  return (
    <div>
      <button
        onClick={() => navigate("/")}
        className="mb-6 flex items-center gap-2 text-gray-600 hover:text-gray-900"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to repositories
      </button>

      <RepositoryDetails
        repository={repository}
        fileStats={fileStats}
        onGenerateDigest={generateDigest}
      />
    </div>
  );
}
