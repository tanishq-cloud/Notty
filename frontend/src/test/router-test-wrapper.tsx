// Import the generated route tree
import { routeTree } from "../routeTree.gen";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  RouterProvider,
  createRouter,
  createMemoryHistory,
} from "@tanstack/react-router";
import { render } from "@testing-library/react";

export function renderRoute(route: string) {
  const testQueryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  const memoryHistory = createMemoryHistory({
    initialEntries: [route],
  });

  const router = createRouter({
    routeTree,
    defaultNotFoundComponent: () => <div> Not found </div>,
    context: {
      queryClient: testQueryClient,
    },
    defaultPreload: "intent", // not sure if I need this or the next line
    defaultPreloadStaleTime: 0,
    history: memoryHistory, // also not sure if this is necessary but probably is
  });

  const { rerender, ...result } = render(
    <QueryClientProvider client={testQueryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>,
  );

  return {
    ...result,
    rerender: () =>
      // not exactly sure what this rerender property or function is or if I need it
      rerender(
        <QueryClientProvider client={testQueryClient}>
          <RouterProvider router={router} />
        </QueryClientProvider>,
      ),
  };
}
