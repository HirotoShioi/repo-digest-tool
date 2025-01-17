import { screen } from "@testing-library/react";
import { render } from "../test-utils";
import { describe, it, expect } from "vitest";
import "@testing-library/jest-dom";
import { RepositoryList } from "@/components/home/repository-list";
import { Repository } from "@/types";

describe("RepositoryList", () => {
  const mockRepositories: Repository[] = [
    {
      name: "test-repo-1",
      author: "test-author-1",
      url: "https://github.com/test-author-1/test-repo-1",
      branch: "main",
      updatedAt: new Date("2023-12-18T12:00:00Z"),
      id: "1",
      path: "test-path-1",
      size: 100,
    },
    {
      name: "test-repo-2",
      author: "test-author-2",
      url: "https://github.com/test-author-2/test-repo-2",
      branch: "main",
      updatedAt: new Date("2023-12-18T12:00:00Z"),
      id: "2",
      path: "test-path-2",
      size: 200,
    },
  ];

  it("renders repository cards for each repository", () => {
    render(<RepositoryList repositories={mockRepositories} />);

    mockRepositories.forEach((repo) => {
      expect(screen.getByText(repo.name)).toBeInTheDocument();
      expect(screen.getByText(repo.url)).toBeInTheDocument();
    });
  });

  it("displays empty state message when no repositories", () => {
    render(<RepositoryList repositories={[]} />);

    expect(
      screen.getByText(
        "No repositories added yet. Add one using the form above."
      )
    ).toBeInTheDocument();
  });
});
