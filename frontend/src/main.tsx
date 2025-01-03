import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import "./index.css";
import Providers from "@/providers";
import { RouterProvider, createRouter } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { FullScreenLoader } from "./components/full-screen-loader";
import { ErrorPage } from "./components/error-page";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
});

// Create a new router instance
const router = createRouter({
  routeTree,
  context: {
    queryClient,
  },
  defaultPreload: "intent",
  defaultPreloadStaleTime: 0,
  defaultPendingComponent: () => <FullScreenLoader label="Loading..." />,
  defaultErrorComponent: ({ error }: { error: Error }) => (
    <ErrorPage error={error} />
  ),
});

// Register the router instance for type safety
declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <Providers>
        <RouterProvider router={router} defaultPreload="intent" />
      </Providers>
    </QueryClientProvider>
  </StrictMode>
);
