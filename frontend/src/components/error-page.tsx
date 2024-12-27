import { Link } from "@tanstack/react-router";
import { AlertTriangle } from "lucide-react";

type ErrorPageProps = {
  error?: Error;
};

export const ErrorPage = ({ error }: ErrorPageProps) => {
  return (
    <div className="flex items-center justify-center p-4">
      <div className="text-center">
        <AlertTriangle className="h-16 w-16 text-destructive mx-auto mb-4" />
        <h1 className="text-2xl font-semibold mb-2">Something went wrong</h1>
        <p className="text-muted-foreground mb-6">
          {error?.message || "An unexpected error occurred"}
        </p>
        <Link
          to="/"
          className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
        >
          Return to Home
        </Link>
      </div>
    </div>
  );
};
