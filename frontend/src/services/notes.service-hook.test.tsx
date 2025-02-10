import { describe, it, expect, vi } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useNotes } from "./notes.service-hook";
import * as notesService from "@/services/notes.service";

// Mock the notes service
vi.mock("@/services/notes.service");

describe("useNotes hook", () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    // Create a new QueryClient for each test
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );

  // Test Fetching Notes
  it("should fetch notes successfully", async () => {
    // Prepare mock data
    const mockNotes = [
      { id: 1, title: "Test Note 1", content: "Content 1" },
      { id: 2, title: "Test Note 2", content: "Content 2" },
    ];

    // Mock the getNotes service method
    vi.mocked(notesService.getNotes).mockResolvedValue(mockNotes);

    // Render the hook
    const { result } = renderHook(() => useNotes(), { wrapper });

    // Wait for the query to resolve
    await waitFor(() => {
      return result.current.notes !== undefined;
    });

    // Assertions
    expect(result.current.isLoading).toBe(false);
    expect(result.current.isError).toBe(false);
    expect(result.current.notes).toEqual(mockNotes);
  });

  // Test Creating a Note
  it("should create a note successfully", async () => {
    // Prepare mock data
    const newNote = {
      note_id: 1,
      title: "Test Note",
      body: "<p>Note body</p>",
      author: 1,
      created: new Date().toISOString(),
      modified: new Date().toISOString(),
    };

    // Mock the createNote service method
    vi.mocked(notesService.createNote).mockResolvedValue(newNote);
    vi.mocked(notesService.getNotes).mockResolvedValue([newNote]);

    // Render the hook
    const { result } = renderHook(() => useNotes(), { wrapper });

    // Perform create mutation
    await result.current.createMutation.mutateAsync(newNote);

    // Verify mutation success
    await waitFor(() => {
      expect(notesService.createNote).toHaveBeenCalledWith(newNote);
      expect(result.current.createMutation.isSuccess).toBe(true);
    });
  });

  // Test Updating a Note
  it("should update a note successfully", async () => {
    // Prepare mock data
    const existingNote = {
      id: 1,
      title: "Original Title",
      content: "Original Content",
    };
    const updatedData = { title: "Updated Title" };

    // Mock the updateNote service method
    vi.mocked(notesService.updateNote).mockResolvedValue({
      ...existingNote,
      ...updatedData,
    });
    vi.mocked(notesService.getNotes).mockResolvedValue([
      {
        ...existingNote,
        ...updatedData,
      },
    ]);

    // Render the hook
    const { result } = renderHook(() => useNotes(), { wrapper });

    // Perform update mutation
    await result.current.updateMutation.mutateAsync({
      noteId: existingNote.id,
      updatedData,
    });

    // Verify mutation success
    await waitFor(() => {
      expect(notesService.updateNote).toHaveBeenCalledWith(
        existingNote.id,
        updatedData,
      );
      expect(result.current.updateMutation.isSuccess).toBe(true);
    });
  });

  // Test Deleting a Note
  it("should delete a note successfully", async () => {
    // Prepare mock data
    const noteToDelete = {
      note_id: 1,
      title: "Test Note",
      body: "<p>Note body</p>",
      author: 1,
      created: new Date().toISOString(),
      modified: new Date().toISOString(),
    };

    // Mock the deleteNote service method
    vi.mocked(notesService.deleteNote).mockResolvedValue(undefined);
    vi.mocked(notesService.getNotes).mockResolvedValue([]);

    // Render the hook
    const { result } = renderHook(() => useNotes(), { wrapper });

    // Perform delete mutation
    await result.current.deleteMutation.mutateAsync(noteToDelete.note_id);

    // Verify mutation success
    await waitFor(() => {
      expect(notesService.deleteNote).toHaveBeenCalledWith(
        noteToDelete.note_id,
      );
      expect(result.current.deleteMutation.isSuccess).toBe(true);
    });
  });

  // Test Error Handling
  it("should handle errors when creating a note", async () => {
    // Prepare mock error
    const mockError = new Error("Creation failed");

    // Mock the createNote service method to throw an error
    vi.mocked(notesService.createNote).mockRejectedValue(mockError);

    // Render the hook
    const { result } = renderHook(() => useNotes(), { wrapper });

    // Attempt to create note and catch error
    try {
      await result.current.createMutation.mutateAsync({
        note_id: 1,
        title: "Failed Note",
        body: "<p>Note body</p>",
        author: 1,
        created: new Date().toISOString(),
        modified: new Date().toISOString(),
      });
    } catch (error) {
      expect(error).toEqual(mockError);
    }

    // Verify error state
    await waitFor(() => {
      expect(result.current.createMutation.isError).toBe(true);
    });
  });
});
