import { renderRoute } from "@/test/router-test-wrapper";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import { useNotes } from "@/services/notes.service-hook";
import NotesPage from "@/pages/notes-page";
import { useAuth } from "@/hooks/use-auth";
import * as notesService from "@/services/notes.service-hook";

// Mocking hooks and services
vi.mock("@/services/notes.service-hook");
vi.mock("@/hooks/use-auth");

describe("NotesPage", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("renders notes list when authenticated and data is fetched", async () => {
    const mockNotes = [{ note_id: "1", title: "Test Note", body: "<p>Note body</p>" }];
    useNotes.mockReturnValue({ notes: mockNotes, isLoading: false, isError: false });
    useAuth.mockReturnValue(true); // authenticated user

    renderRoute("/notes");

    // Check if notes are displayed
    await waitFor(() => {
      expect(screen.getByText(/Test Note/)).toBeInTheDocument();
    });
  });

  it("redirects to login page when not authenticated", async () => {
    useAuth.mockReturnValue(false); // not authenticated

    renderRoute("/notes");

    // Check if user is redirected
    await waitFor(() => {
      expect(window.location.pathname).toBe("/login");
    });
  });

  it("shows loading state while fetching notes", async () => {
    useNotes.mockReturnValue({ notes: [], isLoading: true, isError: false });
    useAuth.mockReturnValue(true); // authenticated user

    renderRoute("/notes");

    // Check if loading message is shown
    expect(screen.getByText(/Loading notes.../)).toBeInTheDocument();
  });

  it("shows error message when failed to fetch notes", async () => {
    useNotes.mockReturnValue({ notes: [], isLoading: false, isError: true });
    useAuth.mockReturnValue(true); // authenticated user

    renderRoute("/notes");

    // Check if error message is shown
    expect(screen.getByText(/Error loading notes. Please try again later./)).toBeInTheDocument();
  });
});
