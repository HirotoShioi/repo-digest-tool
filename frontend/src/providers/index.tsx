import { TooltipProvider } from "@radix-ui/react-tooltip";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { Toaster } from "@/components/ui/toaster";

function Provider({ children }: { children: React.ReactNode }) {
  return (
    <TooltipProvider delayDuration={0}>
      {children}
      <Toaster />
      <ReactQueryDevtools initialIsOpen={false} />
    </TooltipProvider>
  );
}

export default Provider;
