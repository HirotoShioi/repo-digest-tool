import { Loader2 } from "lucide-react";

type FullScreenLoaderProps = {
  message?: string;
};
function FullScreenLoader({ message }: FullScreenLoaderProps) {
  return (
    <div className="flex items-center justify-center h-">
      <Loader2 className="w-4 h-4 animate-spin" />
      {message && <p className="text-muted-foreground">{message}</p>}
    </div>
  );
}

export default FullScreenLoader;
