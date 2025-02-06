import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getNotes, updateNote, deleteNote, createNote } from '@/services/notes.service';
import { Note } from '@/interface/Note';


export const useNotes = () => {
    const queryClient = useQueryClient();

    const { data: notes, isLoading, isError, error, isFetching } = useQuery({
        queryKey: ['notes'],
        queryFn: getNotes,
    });

    const createMutation = useMutation({
        mutationFn: (newNote: Note) => createNote(newNote),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['notes'] });
        },
        onError: (error) => {
            console.error('Failed to create note:', error);
            throw new Error('Unable to create the note. Please try again later');
            
        }
    });

    const updateMutation = useMutation({
        mutationFn: ({ noteId, updatedData }: { noteId: number; updatedData: Partial<Note> }) =>
            updateNote(noteId, updatedData),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['notes'] });
        },
        onError: (error) => {
            console.error('Failed to update note:', error);
            throw new Error('Unable to update the note. Please try again later');
        }
    });

    const deleteMutation = useMutation({
        mutationFn: (noteId: number) => deleteNote(noteId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['notes'] });
        },
        onError: (error) => {
            console.error('Failed to delete note:', error);
            throw new Error('Unable to delete the note. Please try again later.');
        }
    });

    return { 
        notes, 
        isLoading,
        isFetching, 
        isError, 
        error,
        createMutation, 
        updateMutation, 
        deleteMutation 
    };
};