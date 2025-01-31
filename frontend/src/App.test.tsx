import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@/utils/test-utils";
import App from "@/App";

// Mocking components and hooks
vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string) => key,
  }),
}));

vi.mock("./components/LanguageSelector", () => ({
  __esModule: true,
  default: () => <div data-testid="language-selector">Language Selector</div>,
}));

vi.mock("./pages/TableInfiniteDisplay", () => ({
  __esModule: true,
  default: () => <div data-testid="table-infinite-page">Table Infinite Page</div>,
}));

vi.mock("./pages/ChartDisplay", () => ({
  __esModule: true,
  default: () => <div data-testid="chart-dashboard">Chart Dashboard</div>,
}));

vi.mock("./pages/TableDisplay", () => ({
  __esModule: true,
  default: () => <div data-testid="table-page">Table Page</div>,
}));

describe("App Component", () => {
  it("renders the header with the time, date, and logo", () => {
    render(<App />);
    expect(screen.getByAltText("Brain Icon")).toBeInTheDocument();
    expect(screen.getByText("Hoo")).toBeInTheDocument();
    expect(screen.getByTestId("language-selector")).toBeInTheDocument();
    expect(screen.getByText(new RegExp(new Date().toLocaleDateString()))).toBeInTheDocument();
    expect(screen.getByText(new RegExp(new Date().toLocaleTimeString()))).toBeInTheDocument();
  });

  it("renders the footer with the correct text", () => {
    render(<App />);
    expect(screen.getByText("footer_text")).toBeInTheDocument();
    expect(screen.getByText(/© 2025 Hoo/)).toBeInTheDocument();
  });

  it("renders the tabs and switches between them", async () => {
    render(<App />);
    const tableTab = screen.getByRole("table");
    const chartsTab = screen.getByText("charts");
    const paginatedTableTab = screen.getByText("table_with_pagination");

    // Initial state
    expect(screen.getByTestId("table-infinite-page")).toBeInTheDocument();

    // Switch to Charts Tab
    fireEvent.click(chartsTab);
    expect(screen.getByTestId("chart-dashboard")).toBeInTheDocument();

    // Switch to Paginated Table Tab
    fireEvent.click(paginatedTableTab);
    expect(screen.getByTestId("table-page")).toBeInTheDocument();

    // Switch back to Table Tab
    fireEvent.click(tableTab);
    expect(screen.getByTestId("table-infinite-page")).toBeInTheDocument();
  });
});
