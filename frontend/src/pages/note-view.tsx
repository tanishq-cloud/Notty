import {useNotes} from '@/services/notes.service-hook'
import NotesCardView from '@/components/card-view';
import { Note } from '@/interface/Note';


export default function NotesPage() {
    const {notes, isLoading, isError } = useNotes();
    
    if (isLoading) {
        return <div>Loading notes...</div>;
      }
    
      if (isError) {
        return <div>Error loading notes. Please try again later.</div>;
      }

  const handleViewNote = (note: Note) => {
    console.log('Viewing note:', note);
    return true
  };

  const handleEditNote = (note: Note) => {
    console.log('Editing note:', note);
    return true
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">My Notes</h1>
      <NotesCardView
        notes={notes}
        onView={handleViewNote}
        onEdit={handleEditNote}
      />
    </div>
  );
}