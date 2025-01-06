import { render } from "../test-utils";
import { screen } from "@testing-library/react";
import { LoadingButton } from "@/components/loading-button";
import { describe, expect, it } from "vitest";

describe("LoadingButton", () => {
  it("renders button with children when not loading", () => {
    render(<LoadingButton>Click me</LoadingButton>);
    expect(
      screen.getByRole("button", { name: "Click me" })
    ).toBeInTheDocument();
  });

  it("renders loading state with spinner and loading text", () => {
    render(
      <LoadingButton isLoading loadingText="Loading...">
        Click me
      </LoadingButton>
    );
    expect(
      screen.getByRole("button", { name: "Loading..." })
    ).toBeInTheDocument();
    expect(screen.getByRole("button")).toBeDisabled();
  });

  it("is disabled when disabled prop is true", () => {
    render(<LoadingButton disabled>Click me</LoadingButton>);
    expect(screen.getByRole("button")).toBeDisabled();
  });

  it("applies custom className", () => {
    render(<LoadingButton className="custom-class">Click me</LoadingButton>);
    expect(screen.getByRole("button")).toHaveClass("custom-class");
  });

  it("applies variant styles", () => {
    render(<LoadingButton variant="destructive">Click me</LoadingButton>);
    expect(screen.getByRole("button")).toHaveClass("bg-destructive");
  });
});
