import { useState } from "react";
import { Note } from "@/interface/Note";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import RichNote from "./Editor/view-create";


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

  const handleCloseForm = () => {
    setSelectedNote(null);
    setIsViewMode(false);
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

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {notes.map((note) => (
          <Card key={`note-${note.note_id}`} className="shadow-md">
            <CardHeader>
              <CardTitle>
                Note {note.note_id} : {note.title}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-2">
                {convertHtmlToText(note.body).length > 100
                  ? convertHtmlToText(note.body).substring(0, 100) + "..."
                  : convertHtmlToText(note.body)}
              </p>
              <div className="flex justify-end gap-2">
                <Button
                  onClick={() => {
                    setSelectedNote(note);
                    setIsViewMode(true);
                    onView(note);
                  }}
                  variant="outline"
                >
                  View
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
