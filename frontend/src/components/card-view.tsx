import { useState } from "react";
import { Note } from "@/interface/Note";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import RichNote from "./Editor/view-create";
import { useNotes } from "@/services/notes.service-hook";
import { IconFilePencil, IconTrashX, IconEye } from '@tabler/icons-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

const convertHtmlToText = (html: string) => {
  const doc = new DOMParser().parseFromString(html, "text/html");
  return doc.body.textContent || "";
};

interface NotesCardViewProps {
  notes: Note[];
  onView: (note: Note) => void;
  onEdit: (note: Note) => void;
}

export default function NotesCardView({
  notes,
  onView,
  onEdit,
}: NotesCardViewProps) {
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);
  const [isViewMode, setIsViewMode] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [noteToDelete, setNoteToDelete] = useState<Note | null>(null);
  const { deleteMutation } = useNotes();

  const handleCloseForm = () => {
    setSelectedNote(null);
    setIsViewMode(false);
  };

  const handleDeleteClick = (note: Note) => {
    setNoteToDelete(note);
    setIsDeleteDialogOpen(true);
  };

  const handleConfirmDelete = () => {
    if (noteToDelete) {
      deleteMutation.mutate(noteToDelete.note_id);
      setIsDeleteDialogOpen(false);
      setNoteToDelete(null);
    }
  };

  const handleCancelDelete = () => {
    setIsDeleteDialogOpen(false);
    setNoteToDelete(null);
  };

  return (
    <div>
      {selectedNote && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <RichNote
            note={selectedNote}
            onClose={handleCloseForm}
            isView={isViewMode}
          />
        </div>
      )}

      <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Are you sure?</DialogTitle>
            <DialogDescription>
              This action cannot be undone. This will permanently delete the note titled "{noteToDelete?.title}".
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={handleCancelDelete}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleConfirmDelete}>
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {notes.map((note) => (
          <Card key={`note-${note.note_id}`} className="shadow-md">
            <CardHeader>
              <CardTitle>Note: {note.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-2">
                {convertHtmlToText(note.body).length > 100
                  ? convertHtmlToText(note.body).substring(0, 100) + "..."
                  : convertHtmlToText(note.body)}
              </p>
              <div className="flex justify-end gap-2">
                <Button
                  onClick={() => handleDeleteClick(note)}
                  variant="outline"
                  className="text-red-600"
                >
                  <IconTrashX stroke={2} />
                </Button>

                <Button
                  onClick={() => {
                    setSelectedNote(note);
                    setIsViewMode(true);
                    onView(note);
                  }}
                  variant="outline"
                >
                  <IconEye stroke={2} />
                </Button>

                <Button
                  
                  onClick={() => {
                    setSelectedNote(note);
                    setIsViewMode(false);
                    onEdit(note);
                  }}
                >
                  Edit
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}