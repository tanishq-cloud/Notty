import { render } from "@testing-library/react";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import NotesCardView from "@/components/card-view";
// Importing the module

// Define the mock structure for useNotes hook
const mockUseNotes = {
  notes: [
    {
      note_id: 1,
      title: "Test Note",
      body: "<p>Note body</p>",
      author: 1,
      created: new Date().toISOString(),
      modified: new Date().toISOString(),
    },
    {
      note_id: 2,
      title: "Another Test Note",
      body: "<p>Another note body</p>",
      author: 1,
      created: new Date().toISOString(),
      modified: new Date().toISOString(),
    },
  ],
  isLoading: false,
  isError: false,
  error: null,
  createMutation: { mutate: vi.fn() },
  updateMutation: { mutate: vi.fn() },
  deleteMutation: { mutate: vi.fn() },
};

vi.mock("@/services/notes.service-hook", () => ({
  ...vi.importActual("@/services/notes.service-hook"),
  useNotes: vi.fn(() => mockUseNotes), // Explicitly mock the return value of useNotes
}));

describe("NotesCardView", () => {
  it("renders notes in card view", async () => {
    render(
      <NotesCardView
        notes={mockUseNotes.notes}
        onView={vi.fn()}
        onEdit={vi.fn()}
      />,
    );
    screen.debug();
    expect(screen.getByText("Note: Test Note")).toBeInTheDocument();
    expect(screen.getByText("Note: Another Test Note")).toBeInTheDocument();
  });

  it("clicking on view button triggers onView callback", async () => {
    const onViewMock = vi.fn();
    render(
      <NotesCardView
        notes={mockUseNotes.notes}
        onView={onViewMock}
        onEdit={vi.fn()}
      />,
    );
    screen.debug();
    // Click view button
    const viewButtons = screen.getAllByTestId("view-button");

    await userEvent.click(viewButtons[0]);

    // Check if onView was called with the correct note
    await waitFor(() => {
      expect(onViewMock).toHaveBeenCalledWith(mockUseNotes.notes[0]);
    });
  });

  it("clicking on edit button triggers onEdit callback", async () => {
    const onEditMock = vi.fn();
    render(
      <NotesCardView
        notes={mockUseNotes.notes}
        onView={vi.fn()}
        onEdit={onEditMock}
      />,
    );

    // Click edit button
    const editButtons = screen.getAllByRole("button", { name: /edit/i });
    await userEvent.click(editButtons[0]);

    // Check if onEdit was called with the correct note
    await waitFor(() => {
      expect(onEditMock).toHaveBeenCalledWith(mockUseNotes.notes[0]);
    });
  });

  it("clicking on delete button opens the delete confirmation dialog", async () => {
    render(
      <NotesCardView
        notes={mockUseNotes.notes}
        onView={vi.fn()}
        onEdit={vi.fn()}
      />,
    );

    // Click delete button
    const deleteButtons = screen.getAllByTestId("delete-button");

    await userEvent.click(deleteButtons[0]);

    // Check if delete dialog is opened
    expect(screen.getByText(/Are you sure\?/)).toBeInTheDocument();
  });

  it("confirming delete triggers the delete mutation", async () => {
    render(
      <NotesCardView
        notes={mockUseNotes.notes}
        onView={vi.fn()}
        onEdit={vi.fn()}
      />,
    );

    // Click delete button
    const deleteButtons = screen.getAllByTestId("delete-button");

    await userEvent.click(deleteButtons[0]);
    screen.debug();
    // Confirm delete
    await userEvent.click(screen.getByRole("button", { name: /Delete/i }));

    // Check if delete mutation was called with the correct note's id
    await waitFor(() => {
      expect(mockUseNotes.deleteMutation.mutate).toHaveBeenCalledWith(
        mockUseNotes.notes[0].note_id,
      );
    });
  });
});
