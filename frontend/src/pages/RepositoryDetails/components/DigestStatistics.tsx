import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import {
    Table,
    TableBody,
    TableCell,
    TableRow,
} from "@/components/ui/table";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { formatNumber } from "@/utils/formatters";


type FileTypeAggregation = {
    extension: string;
    count: number;
    tokens: number;
};

type Summary = {
  repository: string;
  totalFiles: number;
  totalSizeKb: number;
  averageFileSizeKb: number;
  maxFileSizeKb: number;
  minFileSizeKb: number;
  fileTypes: FileTypeAggregation[];
  contextLength: number;
};


interface DigestStatisticsParams {
    summary: Summary;
}


function DigestStatistics({ summary }: DigestStatisticsParams) {
  return (
    <Card className="p-2">
      <CardHeader className="p-4">
        <CardTitle>Digest Statistics</CardTitle>
      </CardHeader>
      <CardContent className="p-4">
      <Table className="w-full">
        <TableBody>
          <TableRow>
            <TableCell className="font-semibold">
              Context Length (GPT-4o)
            </TableCell>
            <TableCell className="relative">
                <span
                  className={summary.contextLength > 128000 ? "text-destructive" : "text-muted-foreground"}
                >
                  {formatNumber(summary.contextLength)}
                </span>
                {summary.contextLength > 128000 && (
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <span className="text-red-600 underline cursor-help ml-2">?</span>
                    </TooltipTrigger>
                    <TooltipContent className="bg-gray-800 text-white text-sm rounded-md shadow-md px-4 py-2 w-64">
                      The context length exceeds the limit of 128,000 for
                      GPT-4o. Consider reducing the content or splitting it
                      into smaller chunks to fit within the limit.
                    </TooltipContent>
                  </Tooltip>
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
      </CardContent>
    </Card>
  );
};

export default DigestStatistics;