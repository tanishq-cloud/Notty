import { useEffect, useRef } from 'react';
import Quill from 'quill';
import 'quill/dist/quill.snow.css';

interface RTEProps {
  initialContent?: string;
  onChange?: (content: string) => void; // Make onChange optional for view mode
  disabled?: boolean; // Add disabled prop for view mode
}

export default function RichTextEditor({ initialContent, onChange, disabled = false }: RTEProps) {
  const editorRef = useRef<HTMLDivElement>(null);
  const quillInstance = useRef<Quill | null>(null);

  useEffect(() => {
    if (editorRef.current && !quillInstance.current) {
      const toolbarOptions = disabled ? false : [
        ['bold', 'italic', 'underline', 'strike'],
        ['blockquote', 'code-block'],
        [{ 'header': 1 }, { 'header': 2 }],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],
        [{ 'indent': '-1'}, { 'indent': '+1' }],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        [{ 'color': [] }, { 'background': [] }],
        [{ 'align': [] }],
        ['link', 'image'],
        ['clean']
      ];

      quillInstance.current = new Quill(editorRef.current, {
        modules: {
          toolbar: toolbarOptions, // Disable toolbar if in view mode
        },
        theme: 'snow',
        readOnly: disabled, // Set read-only mode if disabled is true
      });

      // Set initial content if provided
      if (initialContent) {
        try {
          const content = JSON.parse(initialContent);
          quillInstance.current.setContents(content);
        } catch (error) {
          console.error('Failed to parse initial content:' + error + 'data: '+ initialContent);
        }
      }

      // Handle content changes (only if not in view mode)
      if (!disabled && onChange) {
        quillInstance.current.on('text-change', () => {
          const contents = quillInstance.current?.getContents();
          onChange(JSON.stringify(contents));
        });
      }
    }

    // Cleanup
    return () => {
      if (quillInstance.current) {
        quillInstance.current.off('text-change');
      }
    };
  }, [initialContent, disabled, onChange]);

  return (
    <div className="border rounded-md">
      <div ref={editorRef} className="h-64" />
    </div>
  );
}