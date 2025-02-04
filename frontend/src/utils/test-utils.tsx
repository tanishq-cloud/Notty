import { cleanup, render } from "@testing-library/react"
import { afterEach} from "vitest"

afterEach(() => {
    cleanup()
})

function customRender(ui: React.ReactElement, options = {}) {
    return render(ui, {
        wrapper: ({ children }) => children,
        ...options,
    })
}

export * from "@testing-library/react"
export { default as userEvent } from "@testing-library/user-event"
export { customRender as render}


import { createRouter, RouterProvider } from "@tanstack/react-router";
import { createMemoryHistory } from "@tanstack/react-router";
const history = createMemoryHistory();
const router = createRouter({ history });

export const RouterTestWrapper = ({ children }) => (
  <RouterProvider router={router}>{children}</RouterProvider>
);
