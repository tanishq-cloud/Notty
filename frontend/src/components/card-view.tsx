import { Note } from '@/interface/Note';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface NotesCardViewProps {
  notes: Note[];
  onView: (note: Note) => void;
  onEdit: (note: Note) => void;
}

export default function NotesCardView({ notes, onView, onEdit }: NotesCardViewProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {notes.map((note) => (
        <Card key={note.noteid} className="shadow-md">
          <CardHeader>
            <CardTitle>Note {note.noteid}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">
              {note.body.length > 100 ? note.body.substring(0, 100) + '...' : note.body}
            </p>
            <div className="flex justify-end gap-2 mt-2">
              <Button onClick={() => onView(note)} variant="outline">View</Button>
              <Button onClick={() => onEdit(note)}>Edit</Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
