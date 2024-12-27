import { LoadingSpinner } from "./loading-spinner";

type FullScreenLoaderProps = {
  label: string;
};
export const FullScreenLoader = ({ label }: FullScreenLoaderProps) => (
  <div className="fixed inset-0 bg-background/50 backdrop-blur-sm z-50 flex items-center justify-center">
    <LoadingSpinner size={48} label={label} />
  </div>
);
