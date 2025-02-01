import { useState } from "react";
import { Button } from "@/components/ui/button";
import RichTextEditor from "@/components/Editor/rich-text-edit";
import { Input } from "@/components/ui/input";
import { Note } from "@/interface/Note";
import { useNotes } from "@/services/notes.service-hook";

export default function RichNote({
  note,
  onClose,
  isView,
}: {
  note?: Note;
  onClose: () => void;
  isView?: boolean;
}) {
  const { createMutation, updateMutation } = useNotes();
  const [title, setTitle] = useState(note?.title || "");
  const [body, setBody] = useState(note?.body || "Start writing here....");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isView) {
      return;
    }

    const noteData: Note = {
      title,
      note_id: note?.note_id || Math.floor(Math.random() * 1000000),
      author: note?.author || Date.now(),
      body,
      created: note?.created || new Date().toISOString(),
      modified: new Date().toISOString(),
    };

    if (note) {
      console.log(noteData);
      updateMutation.mutate({
        noteId: note.note_id,
        updatedData: noteData,
      });
      console.log("Mutation completed");
    } else {
      createMutation.mutate(noteData);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white shadow-md p-6 rounded-lg w-full max-w-4xl h-auto overflow-auto">
        <h2 className="text-lg font-semibold mb-4">
          {isView ? "View Note" : note ? "Edit Note" : "Create New Note"}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            disabled={isView}
          />
          <RichTextEditor
            initialContent={body}
            onChange={(newContent) => setBody(newContent)}
            disabled={isView}
          />
          <div className="flex justify-end space-x-2">
            <Button type="button" variant="outline" onClick={onClose}>
              {isView ? "Close" : "Cancel"}
            </Button>
            {!isView && (
              <Button
                type="submit"
                disabled={createMutation.isPending || updateMutation.isPending}
              >
                {createMutation.isPending || updateMutation.isPending
                  ? note
                    ? "Updating..."
                    : "Saving..."
                  : note
                    ? "Update Note"
                    : "Create Note"}
              </Button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
