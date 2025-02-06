import { useNotes } from "@/services/notes.service-hook";
import NotesCardView from "@/components/card-view";
import { Note } from "@/interface/Note";
import { useAuth } from "@/hooks/use-auth";
import { useNavigate } from "@tanstack/react-router";
import { Suspense, useEffect, Profiler } from "react";
import ClimbingBoxLoader from "react-spinners/ClimbingBoxLoader";
import LoadingScreen from "@/components/loading-screen";

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
    return (
      <div>
        <ClimbingBoxLoader />
        <div>Error loading notes. Please try again later.</div>
      </div>
    );
  }

  const handleViewNote = (note: Note) => {
    console.log("Viewing note:", note);
    return true;
  };

  const handleEditNote = (note: Note) => {
    console.log("Editing note:", note);
    return true;
  };

  type OnRenderCallback = (
    id: string,
    phase: "mount" | "update" | "nested-update" | null,
    actualDuration: number,
    baseDuration: number,
    startTime: number,
    commitTime: number
  ) => void;
  
  // Example usage:
  const onRender: OnRenderCallback = (
    id,
    phase,
    actualDuration,
    baseDuration,
    startTime,
    commitTime
  ) => {
    const humanReadableStartTime = new Date(startTime).toLocaleString();
  const humanReadableCommitTime = new Date(commitTime).toLocaleString();

  console.log(`Component ID: ${id}`);
  console.log(`Phase: ${phase}`);
  console.log(`Actual Duration: ${actualDuration}ms`);
  console.log(`Base Duration: ${baseDuration}ms`);
  console.log(`Start Time: ${humanReadableStartTime}`);
  console.log(`Commit Time: ${humanReadableCommitTime}`);
  };

  return (
    <Profiler id="NotesPage" onRender={onRender}>
      <Suspense fallback={<LoadingScreen />}>
        <div className="justify-start min-h-screen p-4">
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
      </Suspense>
    </Profiler>
  );
}