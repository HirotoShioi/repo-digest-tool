"use client";

import { Loader2 } from "lucide-react";
import { useRef, useEffect, useState } from "react";

interface LoadingSpinnerProps {
  size?: number;
  className?: string;
  minHeight?: number;
  label?: string;
}

export function LoadingSpinner({
  size = 24,
  className = "",
  minHeight = 100,
  label,
}: LoadingSpinnerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [height, setHeight] = useState<number | string>("auto");

  useEffect(() => {
    const updateHeight = () => {
      if (containerRef.current) {
        const parentHeight = containerRef.current.parentElement?.clientHeight;
        setHeight(
          parentHeight && parentHeight > minHeight ? parentHeight : minHeight
        );
      }
    };

    updateHeight();
    window.addEventListener("resize", updateHeight);

    return () => window.removeEventListener("resize", updateHeight);
  }, [minHeight]);

  return (
    <div ref={containerRef} className="w-full" style={{ height }}>
      <div className="flex items-center justify-center w-full h-full flex-col">
        <Loader2
          className={`animate-spin text-primary ${className}`}
          size={size}
        />
        {label && <div className="text-center py-4 text-gray-600">{label}</div>}
      </div>
    </div>
  );
}
