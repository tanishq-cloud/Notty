import { Note } from "@/interface/Note";
import { Button } from "@/components/ui/button";
import { ColumnDef } from "@tanstack/react-table";
import { IconArrowUp } from "@tabler/icons-react";

export const columns: ColumnDef<Note>[] = [
  {
    accessorKey: "noteid",
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
      >
        ID
        <IconArrowUp className="ml-2 h-4 w-4" />
      </Button>
    ),
    cell: (info) => info.getValue(),
  },
  {
    accessorKey: "authored",
    header: "Authored By",
    cell: (info) => info.getValue(),
  },
  {
    accessorKey: "created",
    header: "Created On",
    cell: (info) => info.getValue(),
  },
  {
    accessorKey: "modified",
    header: "Last Modified",
    cell: (info) => info.getValue(),
  },
  {
    accessorKey: "body",
    header: "Body",
    cell: (info) =>
      info.getValue<string>().length > 100
        ? info.getValue<string>().substring(0, 100) + "..."
        : info.getValue(),
  },
  {
    accessorKey: "actions",
    header: "Actions",
    cell: ({ row }) => (
      <div className="flex gap-2">
        <Button variant="outline" onClick={() => console.log("View", row.original)}>View</Button>
        <Button onClick={() => console.log("Edit", row.original)}>Edit</Button>
      </div>
    ),
  },
];