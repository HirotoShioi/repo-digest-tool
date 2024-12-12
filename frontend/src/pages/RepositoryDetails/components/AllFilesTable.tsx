import React, { useState, useMemo } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";


interface AllFilesTableParams {
    allFiles: {
        name: string;
        path: string;
        tokens: number;
    }[];
}

function formatNumber(number: number) {
    return number.toLocaleString();
}

const AllFilesTable: React.FC<AllFilesTableParams> = ({ allFiles }) => {
  const [searchText, setSearchText] = useState("");
  const [displayCount, setDisplayCount] = useState(20);

  const filteredFiles = useMemo(() => {
    const normalizedSearchText = searchText.toLowerCase();
    return allFiles.filter((file) => {
      const fileName = file.name.toLowerCase();
      const filePath = file.path.toLowerCase();
      return (
        fileName.includes(normalizedSearchText) ||
        filePath.includes(normalizedSearchText)
      );
    });
  }, [allFiles, searchText]);

  const displayedFiles = useMemo(() => {
    if (displayCount === -1) {
      return filteredFiles;
    }
    return filteredFiles.slice(0, displayCount);
  }, [filteredFiles, displayCount]);

  const displayedCount = displayedFiles.length;
  const totalCount = filteredFiles.length;

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mt-8">
      <h2 className="text-xl font-semibold mb-4">All Files</h2>

      {/* Search and Display Controls */}
      <div className="flex flex-wrap gap-4 mb-4">
        {/* Search Input */}
        <div className="flex-grow">
          <Input
            type="text"
            placeholder="Search by file name..."
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />
        </div>

        {/* Display Count Selector */}
        <div className="flex items-center gap-2">
          <Label htmlFor="displayCount" className="text-sm text-gray-600">
            Show:
          </Label>
          <Select onValueChange={(value) => setDisplayCount(parseInt(value, 10))}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select a number of files" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="20">20</SelectItem>
              <SelectItem value="50">50</SelectItem>
              <SelectItem value="100">100</SelectItem>
              <SelectItem value="200">200</SelectItem>
              <SelectItem value="-1">All</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <Table className="min-w-full">
          <TableHeader>
            <TableRow>
              <TableHead className="text-left">File Name</TableHead>
              <TableHead className="text-left">Path</TableHead>
              <TableHead className="text-left">Extension</TableHead>
              <TableHead className="text-left">Context Length</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {displayedFiles.map((file, index) => (
              <TableRow key={index} className="hover:bg-gray-50">
                <TableCell>{file.name}</TableCell>
                <TableCell>{file.path}</TableCell>
                <TableCell>{file.path.split(".").pop() || "None"}</TableCell>
                <TableCell>{formatNumber(file.tokens)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/* Pagination Info */}
      <div className="mt-4 text-sm text-gray-600">
        Showing <span id="displayedCount">{displayedCount}</span> of{" "}
        <span id="totalCount">{totalCount}</span> files
      </div>
    </div>
  );
};

export default AllFilesTable;