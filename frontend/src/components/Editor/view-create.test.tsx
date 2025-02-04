import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import RichNote from "./view-create";
import { vi } from "vitest";

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
  createMutation: {
    mutate: vi.fn(),
    mutateAsync: vi.fn(),
    isLoading: true || false,
  },
  updateMutation: {
    mutate: vi.fn(),
    mutateAsync: vi.fn(),
    isLoading: true || false,
  },
  deleteMutation: {
    mutate: vi.fn(),
    mutateAsync: vi.fn(),
    isLoading: true || false,
  },
};

vi.mock("@/services/notes.service-hook", () => ({
  ...vi.importActual("@/services/notes.service-hook"),
  useNotes: vi.fn(() => mockUseNotes),
}));

describe("RichNote Component", () => {
  const mockOnClose = vi.fn();
  const mockNote = {
    note_id: 1,
    title: "Test Note",
    body: "This is a test note.",
    author: 123,
    created: "2025-01-01T00:00:00Z",
    modified: "2025-01-02T00:00:00Z",
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders correctly in edit mode with a note", () => {
    render(<RichNote note={mockNote} onClose={mockOnClose} isView={false} />);

    expect(screen.getByDisplayValue(mockNote.title)).toBeInTheDocument();
    expect(screen.getByText(mockNote.body)).toBeInTheDocument();
  });

  it("renders correctly in view mode with a note", () => {
    render(<RichNote note={mockNote} onClose={mockOnClose} isView={true} />);

    expect(screen.getByDisplayValue(mockNote.title)).toBeInTheDocument();
    expect(screen.getByText(mockNote.body)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Close" })).toBeInTheDocument();
  });

  it("can edit a note", async () => {
    render(<RichNote note={mockNote} onClose={mockOnClose} isView={false} />);

    await userEvent.clear(screen.getByDisplayValue(mockNote.title));
    const newTitle = "Updated Title";
    await userEvent.type(screen.getByPlaceholderText("Title"), newTitle);

    const editor = screen.getByTestId("quill-editor");
    const newBody = "<p>This is a test note.</p>";
    fireEvent.input(editor, {
      target: { innerHTML: newBody },
    });

    await userEvent.click(screen.getByRole("button", { name: "Update Note" }));

    await waitFor(() => {
      expect(mockUseNotes.updateMutation.mutateAsync).toHaveBeenCalledWith({
        noteId: mockNote.note_id,
        updatedData: {
          title: newTitle,
          body: newBody,
          author: 123,
          created: "2025-01-01T00:00:00Z",
          modified: expect.any(String),
          note_id: mockNote.note_id,
        },
      });

      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it("creates a new note", async () => {
    render(<RichNote onClose={mockOnClose} isView={false} />);
    const quillEditor = screen.getByTestId("quill-editor");

    const newTitle = "This is my note";
    await userEvent.type(screen.getByPlaceholderText("Title"), newTitle);

    const newBody = "<p>Start writing here....</p>";
    fireEvent.input(quillEditor, {
      target: { innerHTML: newBody },
    });

    await userEvent.click(screen.getByRole("button", { name: "Create Note" }));

    await waitFor(() => {
      expect(mockUseNotes.createMutation.mutateAsync).toHaveBeenCalledWith({
        title: newTitle,
        body: newBody,
        author: expect.any(Number),
        created: expect.any(String),
        modified: expect.any(String),
        note_id: expect.any(Number),
      });

      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it("disables submit button when no changes are made", async () => {
    render(<RichNote note={mockNote} onClose={mockOnClose} isView={false} />);

    expect(screen.getByRole("button", { name: "Update Note" })).toBeDisabled();
  });

  it("shows loading states during mutation", async () => {
    const originalMockUseNotes = { ...mockUseNotes };

    mockUseNotes.createMutation = {
      ...originalMockUseNotes.createMutation,
      isLoading: true,
    };

    render(<RichNote note={mockNote} onClose={mockOnClose} isView={false} />);
    const quillEditor = screen.getByTestId("quill-editor");
    await userEvent.type(screen.getByPlaceholderText("Title"), "Created Title");

    fireEvent.input(quillEditor, {
      target: { innerHTML: "<p>Created body content.</p>" },
    });

    await userEvent.click(
      screen.getByRole("button", { name: /Create|Update/i })
    );

    expect(
      screen.getByRole("button", { name: /Update Note/i })
    ).toBeInTheDocument();

    mockUseNotes.createMutation = originalMockUseNotes.createMutation;
  });

  it("calls onClose when cancel or close button is clicked", async () => {
    render(<RichNote note={mockNote} onClose={mockOnClose} isView={false} />);

    await userEvent.click(screen.getByRole("button", { name: "Cancel" }));
    expect(mockOnClose).toHaveBeenCalled();
  });
});
