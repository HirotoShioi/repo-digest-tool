import { useParams, useNavigate } from "react-router";
import { useGetRepositoryById } from "@/services/repositories/queries";
import { useGetSummary } from "@/services/summary/queries";
import Report from "./components/Report";

function RepositoryDetailsPage() {
  const { author, name } = useParams<{ author: string; name: string }>();
  if (!author || !name) {
    return <div>Repository not found</div>;
  }
  const navigate = useNavigate();
  const { data: repository, isLoading } = useGetRepositoryById({
    author,
    name,
  });
  const { data: summary } = useGetSummary({
    author,
    repositoryName: name,
  });

  if (isLoading || !summary) {
    return <div>Loading...</div>;
  }

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
    <>
      <Report summary={summary} author={author} repositoryName={name} />
    </>
  );
}

export default RepositoryDetailsPage;
