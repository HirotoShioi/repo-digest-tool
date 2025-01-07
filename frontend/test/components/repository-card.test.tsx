/* eslint-disable @typescript-eslint/no-explicit-any */
import { screen } from "@testing-library/react";
import { render } from "../test-utils";
import { describe, it, vi, expect, beforeEach } from "vitest";
import "@testing-library/jest-dom";
import { RepositoryCard } from "@/components/home/repository-card";
import {
  useDeleteRepository,
  useUpdateRepository,
} from "@/services/repositories/mutations";
import { Repository } from "@/types";
import userEvent from "@testing-library/user-event";

vi.mock("@/services/repositories/mutations", () => ({
  useDeleteRepository: vi.fn(),
  useUpdateRepository: vi.fn(),
}));

describe("RepositoryCard", () => {
  const mockRepository: Repository = {
    name: "test-repo",
    author: "test-author",
    url: "https://github.com/test-author/test-repo",
    branch: "main",
    updatedAt: new Date("2023-12-18T12:00:00Z"),
    id: "1",
    path: "test-path",
    size: 100,
  };

  const mockDeleteMutate = vi.fn();
  const mockUpdateMutate = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    (useDeleteRepository as any).mockReturnValue({
      mutate: mockDeleteMutate,
      isPending: false,
    });
    (useUpdateRepository as any).mockReturnValue({
      mutate: mockUpdateMutate,
      isPending: false,
    });
  });

  it("renders repository information correctly", () => {
    render(<RepositoryCard repository={mockRepository} />);

    expect(screen.getByText(mockRepository.name)).toBeInTheDocument();
    expect(screen.getByText(mockRepository.url)).toBeInTheDocument();
  });

  it("calls delete mutation when delete button is clicked", async () => {
    render(<RepositoryCard repository={mockRepository} />);

    const deleteButton = screen.getByTestId("delete-repository-button");
    await userEvent.click(deleteButton);

    expect(mockDeleteMutate).toHaveBeenCalledWith(
      {
        author: mockRepository.author,
        repositoryName: mockRepository.name,
      },
      expect.any(Object)
    );
  });

  it("calls update mutation when update button is clicked", async () => {
    render(<RepositoryCard repository={mockRepository} />);

    const updateButton = screen.getByTestId("update-repository-button");
    await userEvent.click(updateButton);

    expect(mockUpdateMutate).toHaveBeenCalledWith(
      {
        author: mockRepository.author,
        repositoryName: mockRepository.name,
      },
      expect.any(Object)
    );
  });
});
