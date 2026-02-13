"use client";

import * as React from "react";
import {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import {
  ArrowUpDown,
  ChevronDown,
  MoreHorizontal,
  Search,
  ExternalLink
} from "lucide-react";
import { useRouter } from "next/navigation";

import { Button } from "@/src/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/src/components/ui/dropdown-menu";
import { Input } from "@/src/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/src/components/ui/table";
import { Badge } from "@/src/components/ui/badge";

export type HistoryItem = {
  keyword: string;
  total: number;
  positive_pct: number;
  negative_pct: number;
  neutral_pct: number;
  platforms: string[];
  last_updated: string;
};

export function HistoryTable({ data }: { data: HistoryItem[] }) {
  const router = useRouter();
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  );
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({});
  const [rowSelection, setRowSelection] = React.useState({});

  const columns: ColumnDef<HistoryItem>[] = [
    {
      accessorKey: "keyword",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Keyword
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        );
      },
      cell: ({ row }) => <div className="font-medium ml-4">{row.getValue("keyword")}</div>,
    },
    {
      accessorKey: "total",
      header: "Total Data",
      cell: ({ row }) => <div className="px-4">{row.getValue("total")}</div>,
    },
    {
      accessorKey: "positive_pct",
      header: "Positive",
      cell: ({ row }) => (
        <div className="text-green-600 font-medium">
          {row.getValue("positive_pct")}%
        </div>
      ),
    },
    {
      accessorKey: "negative_pct",
      header: "Negative",
      cell: ({ row }) => (
        <div className="text-red-600 font-medium">
          {row.getValue("negative_pct")}%
        </div>
      ),
    },
    {
      accessorKey: "neutral_pct",
      header: "Neutral",
      cell: ({ row }) => (
        <div className="text-gray-500 font-medium">
          {row.getValue("neutral_pct")}%
        </div>
      ),
    },
    {
      accessorKey: "platforms",
      header: "Platforms",
      cell: ({ row }) => {
        const platforms = row.getValue("platforms") as string[];
        return (
          <div className="flex gap-1 flex-wrap">
            {platforms.map((p) => (
              <Badge key={p} variant="outline" className="uppercase text-[10px]">
                {p}
              </Badge>
            ))}
          </div>
        );
      },
    },
    {
      accessorKey: "last_updated",
      header: "Last Updated",
      cell: ({ row }) => {
        const date = new Date(row.getValue("last_updated"));
        return <div className="text-xs text-muted-foreground">{date.toLocaleString()}</div>;
      },
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const item = row.original;
  
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <span className="sr-only">Open menu</span>
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuItem
                onClick={() => router.push(`/dashboard?keyword=${item.keyword}`)}
              >
                <ExternalLink className="mr-2 h-4 w-4" />
                View Analysis
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
    },
  ];

  const table = useReactTable({
    data,
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  });

  return (
    <div className="w-full">
      <div className="flex items-center py-4">
        <Input
          placeholder="Filter keywords..."
          value={(table.getColumn("keyword")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("keyword")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
        />
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="ml-auto">
              Columns <ChevronDown className="ml-2 h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {table
              .getAllColumns()
              .filter((column) => column.getCanHide())
              .map((column) => {
                return (
                  <DropdownMenuCheckboxItem
                    key={column.id}
                    className="capitalize"
                    checked={column.getIsVisible()}
                    onCheckedChange={(value) =>
                      column.toggleVisibility(!!value)
                    }
                  >
                    {column.id}
                  </DropdownMenuCheckboxItem>
                );
              })}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <div className="space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
