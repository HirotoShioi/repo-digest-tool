import { TooltipProvider } from "@radix-ui/react-tooltip";

export function Provider({ children }: { children: React.ReactNode }) {
  return <TooltipProvider>{children}</TooltipProvider>;
}
