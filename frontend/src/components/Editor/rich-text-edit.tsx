import { useEffect, useRef } from "react";
import Quill from "quill";
import "quill/dist/quill.snow.css";

interface RTEProps {
  initialContent?: string;
  onChange?: (content: string) => void;
  disabled?: boolean;
}

export default function RichTextEditor({
  initialContent = "",
  onChange,
  disabled = false,
}: RTEProps) {
  const editorRef = useRef<HTMLDivElement>(null);
  const quillInstance = useRef<Quill | null>(null);

  useEffect(() => {
    if (editorRef.current && !quillInstance.current) {
      quillInstance.current = new Quill(editorRef.current, {
        theme: "snow",
        readOnly: disabled,
        modules: {
          toolbar: disabled
            ? false
            : [
                ["bold", "italic", "underline", "strike"],
                [{ header: 1 }, { header: 2 }],
                [{ list: "ordered" }, { list: "bullet" }],
                [{ script: "sub" }, { script: "super" }],
                [{ indent: "-1" }, { indent: "+1" }],
                [{ color: [] }, { background: [] }],
                [{ align: [] }],
                ["link", "image"],
                ["clean"],
              ],
        },
      });

      if (initialContent) {
        quillInstance.current.root.innerHTML = initialContent; 
      }

      if (!disabled && onChange) {
        quillInstance.current.on("text-change", () => {
          onChange(quillInstance.current!.root.innerHTML); 
        });
      }
    }
  }, [initialContent, disabled, onChange]);

  return (
    <div className="border rounded-md">
      <div
        ref={editorRef}
        className="h-64 max-h-64 overflow-auto" 
      />
    </div>
  );
}
