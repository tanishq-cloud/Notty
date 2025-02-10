import { createLazyFileRoute } from "@tanstack/react-router";
import NotesPage from "@/pages/note-view/note-view";

export const Route = createLazyFileRoute("/list")({
  component: NotesPage,
});
