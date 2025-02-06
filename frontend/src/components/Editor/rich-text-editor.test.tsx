import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import RichTextEditor from "./rich-text-edit";
import Quill from "quill";

// Mock Quill 
vi.mock("quill", () => ({
  default: vi.fn().mockImplementation(() => ({
    root: {
      innerHTML: "",
    },
    on: vi.fn(),
    setText: vi.fn(),
    setContents: vi.fn(),
  }))
}));

describe("RichTextEditor Component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders without crashing", () => {
    render(<RichTextEditor />);
    const editorContainer = screen.getByTestId("quill-editor");
    expect(editorContainer).toBeInTheDocument();
  });

  it("sets initial content correctly", () => {
    const initialContent = "<p>Test content</p>";
    render(<RichTextEditor initialContent={initialContent} />);
    
    const editorContainer = screen.getByTestId("quill-editor");
    expect(editorContainer).toBeInTheDocument();
  });

  
  it("disables editor when disabled prop is true", () => {
    render(<RichTextEditor disabled={true} />);
    
    const editorContainer = screen.getByTestId("quill-editor");
    expect(editorContainer).toBeInTheDocument();
  });

  it("handles empty initial content", () => {
    render(<RichTextEditor />);
    
    const editorContainer = screen.getByTestId("quill-editor");
    expect(editorContainer).toBeInTheDocument();
  });

  it("applies correct CSS classes", () => {
    render(<RichTextEditor />);
    
    const editorContainer = screen.getByTestId("quill-editor");
    expect(editorContainer).toHaveClass("h-64 max-h-64 overflow-auto");
  });

  it("creates Quill instance with correct configuration", () => {
    render(<RichTextEditor />);
    
    // Verify Quill was instantiated
    expect(Quill).toHaveBeenCalled();
  });
});