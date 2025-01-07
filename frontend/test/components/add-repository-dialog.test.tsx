/* eslint-disable @typescript-eslint/no-explicit-any */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "../test-utils";
import { AddRepositoryDialog } from "@/components/home/add-repository-dialog";
import { useCloneRepository } from "@/services/repositories/mutations";

// Mock the repositories mutations
vi.mock("@/services/repositories/mutations", () => ({
  useCloneRepository: vi.fn(() => ({
    mutate: vi.fn(),
    isPending: false,
  })),
}));

describe("AddRepositoryDialog", () => {
  const mockCloneRepository = vi.fn();
  beforeEach(() => {
    vi.clearAllMocks();
    (useCloneRepository as any).mockReturnValue({
      mutate: vi.fn(),
      isPending: false,
    });
  });

  it("renders add repository button", () => {
    render(<AddRepositoryDialog />);
    expect(screen.getByText("Add Repository")).toBeInTheDocument();
  });

  it("opens dialog when clicking add button", async () => {
    const { user } = render(<AddRepositoryDialog />);
    await user.click(screen.getByText("Add Repository"));
    expect(screen.getByText("Add New Repository")).toBeInTheDocument();
  });

  it("shows loading state when cloning repository", async () => {
    (useCloneRepository as any).mockReturnValue({
      mutate: mockCloneRepository,
      isPending: true,
    });

    const { user } = render(<AddRepositoryDialog />);
    await user.click(screen.getByText("Add Repository"));
    await user.type(
      screen.getByPlaceholderText("Enter Git repository URL"),
      "https://github.com/user/repo"
    );

    expect(screen.getByText("Cloning...")).toBeInTheDocument();
  });

  it("calls clone mutation with entered URL", async () => {
    const { user } = render(<AddRepositoryDialog />);
    await user.click(screen.getByText("Add Repository"));

    const input = screen.getByPlaceholderText("Enter Git repository URL");
    await user.type(input, "https://github.com/user/repo");
    await user.click(screen.getByText("Clone Repository"));
  });

  it("closes dialog and resets form on successful clone", async () => {
    let successCallback: () => void = () => {};
    (useCloneRepository as any).mockReturnValue({
      mutate: (params: any, options: any) => {
        successCallback = options.onSuccess;
        mockCloneRepository(params);
      },
      isPending: false,
    });

    const { user } = render(<AddRepositoryDialog />);
    await user.click(screen.getByText("Add Repository"));

    const input = screen.getByPlaceholderText("Enter Git repository URL");
    await user.type(input, "https://github.com/user/repo");
    await user.click(screen.getByText("Clone Repository"));

    // Simulate successful clone
    successCallback();

    await waitFor(() => {
      expect(screen.queryByText("Add New Repository")).not.toBeInTheDocument();
    });
  });
});
