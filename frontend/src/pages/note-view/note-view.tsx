import { useNotes } from "@/services/notes.service-hook";
import NotesCardView from "@/components/card-view";
import { Note } from "@/interface/Note";
import { useAuth } from "@/hooks/use-auth";
import { useNavigate } from "@tanstack/react-router";
import { useEffect } from "react";

export default function NotesPage() {
  const { notes, isLoading, isError } = useNotes();
  const authenticated = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!authenticated) {
      navigate({ to: "/login" });
    }
  }, [authenticated, navigate]);

  if (!authenticated) {
    return null;
  }
  if (isLoading) {
    return <div>Loading notes...</div>;
  }

  if (isError) {
    return <div>Error loading notes. Please try again later.</div>;
  }

  const handleViewNote = (note: Note) => {
    console.log("Viewing note:", note);
    return true;
  };

  const handleEditNote = (note: Note) => {
    console.log("Editing note:", note);
    return true;
  };

  return (
    <div className=" justify-start min-h-screen p-4">
      <h1 className="text-2xl font-bold mb-4 self-start">My Notes</h1>

      {notes.length === 0 ? (
        <p className="text-gray-500 text-lg">No note has been created</p>
      ) : (
        <NotesCardView
          notes={notes}
          onView={handleViewNote}
          onEdit={handleEditNote}
        />
      )}
    </div>
  );
}
