import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import RichNote from "./view-create";
import { useNotes } from "@/services/notes.service-hook";
import { vi } from "vitest";



const mockUseNotes = {
    notes: [
      { note_id: 1, title: "Test Note", body: "<p>Note body</p>", author: 1, created: new Date().toISOString(), modified: new Date().toISOString() },
      { note_id: 2, title: "Another Test Note", body: "<p>Another note body</p>", author: 1, created: new Date().toISOString(), modified: new Date().toISOString() },
    ],
    isLoading: false,
    isError: false,
    error: null,
    createMutation: { mutate: vi.fn(),mutateAsync: vi.fn() },
    updateMutation: { mutate: vi.fn(), mutateAsync: vi.fn() },
    deleteMutation: { mutate: vi.fn(), mutateAsync: vi.fn() },
  };
  
  vi.mock("@/services/notes.service-hook", () => ({
    ...vi.importActual("@/services/notes.service-hook"),
    useNotes: vi.fn(() => mockUseNotes),  // Explicitly mock the return value of useNotes
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

    // Mocking useNotes return value using vi.fn()
    useNotes.mockImplementation(() => ({
      createMutation: {
        mutateAsync: vi.fn()
      },
      updateMutation: {
        mutateAsync: vi.fn()
      },
      deleteMutation: {
        mutateAsync: vi.fn()
      },
      notes: [],
      isLoading: false,
      isError: false,
      error: null,
    }));
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
  
    // Clear and update title
    await userEvent.clear(screen.getByDisplayValue(mockNote.title));
    await userEvent.type(screen.getByPlaceholderText("Title"), "Updated Title");
  
    // For Quill RTE, use a more specific method to set content
    const editor = screen.getByTestId('quill-editor'); // Assumes you've added a data-testid to the Quill editor
    
    // Method 1: If the component exposes a way to set Quill content
    await userEvent.type(editor, "Updated body content.");
  
    // Alternative Method 2: If using direct Quill instance manipulation
    // This requires mocking the Quill instance or using a ref in the component
    // fireEvent.input(editor, { target: { innerHTML: 'Updated body content.' } });
  
    // Submit form
    await userEvent.click(screen.getByRole("button", { name: "Update Note" }));
  
    // Check if updateMutation was called with correct data
    await waitFor(() => {
      expect(mockUseNotes.updateMutation.mutateAsync).toHaveBeenCalledWith({
        noteId: mockNote.note_id,
        updatedData: {
          ...mockNote,
          title: "Updated Title",
          body: "Updated body content.",
          modified: expect.any(String),
        },
      });
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it("creates a new note", async () => {
    render(<RichNote onClose={mockOnClose} isView={false} />);

    // Type new title and body
    const newTitle = "New Note";
    await userEvent.type(screen.getByPlaceholderText("Title"), newTitle);

    const newBody = "This is a new note body.";
    await userEvent.type(screen.getByPlaceholderText("Start writing here...."), newBody);

    // Submit form
    await userEvent.click(screen.getByRole("button", { name: "Create Note" }));

    // Check if createMutation was called with correct data
    await waitFor(() => {
      expect(useNotes().createMutation.mutateAsync).toHaveBeenCalledWith({
        title: newTitle,
        note_id: expect.any(Number), // random id
        author: expect.any(Number),
        body: newBody,
        created: expect.any(String),
        modified: expect.any(String),
      });
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it("disables submit button when no changes are made", async () => {
    render(<RichNote note={mockNote} onClose={mockOnClose} isView={false} />);

    // Ensure the submit button is disabled if no changes are made
    expect(screen.getByRole("button", { name: "Update Note" })).toBeDisabled();
  });

  it("shows loading states during mutation", async () => {
    // Simulate a loading state by mocking isLoading to be true
    // useNotes.mockImplementationOnce(() => ({
    //   createMutation: {
    //     mutateAsync: vi.fn(),
      
    //   },
    //   updateMutation: {
    //     mutateAsync: vi.fn(),
       
    //   },
    //   deleteMutation: {
    //     mutateAsync: vi.fn(),
    //     isLoading: false,
    //   },
    //   notes: [],
    //   isLoading: false,
    //   isError: false,
    //   error: null,
    // }));
   

    render(<RichNote note={mockNote} onClose={mockOnClose} isView={false} />);

    // Check if "Saving..." or "Updating..." is shown based on the state
    expect(screen.getByRole("button", { name: "Saving..." })).toBeInTheDocument();
  });

  it("calls onClose when cancel or close button is clicked", async () => {
    render(<RichNote note={mockNote} onClose={mockOnClose} isView={false} />);

    await userEvent.click(screen.getByRole("button", { name: "Cancel" }));
    expect(mockOnClose).toHaveBeenCalled();
  });
});
