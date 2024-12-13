import { useState, useMemo } from "react";
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { FileData } from "@/types";
import { formatNumber } from "@/utils/formatters";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { useExcludeFiles } from "@/services/settings/mutations";
import { useToast } from "@/hooks/use-toast";

interface AllFilesTableParams {
  fileData: FileData[];
  author: string;
  name: string;
}

function AllFilesTable({ fileData, author, name }: AllFilesTableParams) {
  const { mutate: excludeFiles } = useExcludeFiles();
  const [searchText, setSearchText] = useState("");
  const [displayCount, setDisplayCount] = useState(20);
  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set());

  const filteredFiles = useMemo(() => {
    const normalizedSearchText = searchText.toLowerCase();
    return fileData.filter((file) => {
      const fileName = file.name.toLowerCase();
      const filePath = file.path.toLowerCase();
      return (
        fileName.includes(normalizedSearchText) ||
        filePath.includes(normalizedSearchText)
      );
    });
  }, [fileData, searchText]);

  const displayedFiles = useMemo(() => {
    if (displayCount === -1) {
      return filteredFiles;
    }
    return filteredFiles.slice(0, displayCount);
  }, [filteredFiles, displayCount]);

  const displayedCount = displayedFiles.length;
  const totalCount = filteredFiles.length;

  const handleCheckboxChange = (filePath: string) => {
    setSelectedFiles((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(filePath)) {
        newSet.delete(filePath);
      } else {
        newSet.add(filePath);
      }
      return newSet;
    });
  };

  const { toast } = useToast();
  const handleFilterClick = () => {
    excludeFiles(
      {
        author,
        name,
        paths: Array.from(selectedFiles),
      },
      {
        onError: (error) => {
          toast({
            title: "Failed to exclude files",
            description: error.message,
            variant: "destructive",
          });
        },
        onSuccess: () => {
          toast({
            title: "Files excluded",
          });
        },
      }
    );
    setSelectedFiles(new Set());
  };

  return (
    <Card className="p-2 mt-8">
      <CardHeader className="p-4">
        <CardTitle>All Files</CardTitle>
      </CardHeader>
      <CardContent className="p-4">
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

          {/* Add Filter Button */}
          <Button
            onClick={handleFilterClick}
            disabled={selectedFiles.size === 0}
            variant="secondary"
          >
            Filter ({selectedFiles.size})
          </Button>

          {/* Display Count Selector */}
          <div className="flex items-center gap-2">
            <Label htmlFor="displayCount" className="text-sm text-gray-600">
              Show:
            </Label>
            <Select
              onValueChange={(value) => setDisplayCount(parseInt(value, 10))}
            >
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

        <div className="overflow-x-auto">
          <Table className="min-w-full">
            <TableHeader>
              <TableRow>
                <TableHead className="w-[50px]"></TableHead>
                <TableHead className="text-left">File Name</TableHead>
                <TableHead className="text-left">Path</TableHead>
                <TableHead className="text-left">File Type</TableHead>
                <TableHead className="text-left">Context Length</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {displayedFiles.map((file, index) => (
                <TableRow key={index} className="hover:bg-muted">
                  <TableCell>
                    <Checkbox
                      checked={selectedFiles.has(file.path)}
                      onCheckedChange={() => handleCheckboxChange(file.path)}
                    />
                  </TableCell>
                  <TableCell>{file.name}</TableCell>
                  <TableCell>{file.path}</TableCell>
                  <TableCell>{file.extension || "None"}</TableCell>
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
      </CardContent>
    </Card>
  );
}

export default AllFilesTable;
