import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function extractAuthorAndNameFromUrl(url: string): {
  author?: string;
  name?: string;
} | null {
  try {
    const urlObj = new URL(url);
    const author = urlObj.pathname.split("/")[1];
    const name = urlObj.pathname.split("/")[2];
    return { author, name };
  } catch (error) {
    console.error(error);
    return null;
  }
}
