import React from "react";
import {
    Table,
    TableBody,
    TableCell,
    TableRow,
} from "@/components/ui/table";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";


interface DigestStatisticsParams {
    summary: {
        contextLength: number;
        totalFiles: number;
        totalSizeKb: number;
        averageFileSizeKb: number;
        maxFileSizeKb: number;
        minFileSizeKb: number;
    };
}

function formatNumber(number: number) {
    return number.toLocaleString();
}

const DigestStatistics: React.FC<DigestStatisticsParams> = ({ summary }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Digest Statistics</h2>
      <Table className="w-full">
        <TableBody>
          <TableRow>
            <TableCell className="font-semibold">
              Context Length (GPT-4o)
            </TableCell>
            <TableCell className="relative">
                    <span
                      className={summary.contextLength > 128000 ? "text-red-600" : "text-gray-800"}
                    >
                      {formatNumber(summary.contextLength)}
                    </span>
                    {summary.contextLength > 128000 && (
                       <TooltipProvider>
                            <Tooltip>
                                <TooltipTrigger asChild>
                                  <span className="text-red-600 underline cursor-help">?</span>
                                </TooltipTrigger>
                                <TooltipContent className="bg-gray-800 text-white text-sm rounded-md shadow-md px-4 py-2 w-64">
                                  The context length exceeds the limit of 128,000 for
                                  GPT-4o. Consider reducing the content or splitting it
                                  into smaller chunks to fit within the limit.
                                </TooltipContent>
                           </Tooltip>
                       </TooltipProvider>
                    )}
                </TableCell>
          </TableRow>
          <TableRow>
            <TableCell className="font-semibold">Total Files</TableCell>
            <TableCell>{formatNumber(summary.totalFiles)}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell className="font-semibold">Total Size</TableCell>
            <TableCell>{formatNumber(summary.totalSizeKb)} KB</TableCell>
          </TableRow>
          <TableRow>
            <TableCell className="font-semibold">Average File Size</TableCell>
            <TableCell>
              {formatNumber(summary.averageFileSizeKb)} KB
            </TableCell>
          </TableRow>
          <TableRow>
            <TableCell className="font-semibold">Max File Size</TableCell>
            <TableCell>{formatNumber(summary.maxFileSizeKb)} KB</TableCell>
          </TableRow>
          <TableRow>
            <TableCell className="font-semibold">Min File Size</TableCell>
            <TableCell>{formatNumber(summary.minFileSizeKb)} KB</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  );
};

export default DigestStatistics;