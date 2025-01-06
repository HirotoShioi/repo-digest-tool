import { render, RenderOptions, screen, waitFor } from "@testing-library/react";
import Providers from "@/providers";
import {
  createMemoryHistory,
  createRootRoute,
  createRoute,
  createRouter,
  Outlet,
  RouterProvider,
} from "@tanstack/react-router";
import { ReactElement } from "react";
import userEvent from "@testing-library/user-event";

interface TestRouterProviderProps {
  component: () => React.ReactNode;
}

function TestRouterProvider({ component }: TestRouterProviderProps) {
  const rootRoute = createRootRoute({
    component: Outlet,
  });

  const indexRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/",
    component,
  });

  const routeTree = rootRoute.addChildren([indexRoute]);
  const history = createMemoryHistory({ initialEntries: ["/"] });
  const router = createRouter({ routeTree, history });

  /* @ts-expect-error router */
  return <RouterProvider router={router} />;
}

type RenderReturn = ReturnType<typeof render> & {
  user: ReturnType<typeof userEvent.setup>;
};
export function customRender(
  ui: ReactElement,
  options?: Omit<RenderOptions, "wrapper">
): RenderReturn {
  const user = userEvent.setup();
  const result = render(
    <TestRouterProvider component={() => <Providers>{ui}</Providers>} />,
    {
      ...options,
    }
  );
  return { user, ...result };
}

export { customRender as render, screen, waitFor };
