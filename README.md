# Repo Digest Tool: Features and Usage Guide

<img src="./examples/スクリーンショット%202024-12-15%206.58.15.png" alt="Repo Digest Tool Screenshot" style="width: 100%; max-width: 800px;" />

## Features Overview

The **Repo Digest Tool** serves a single, focused purpose: to compress the entirety of a GitHub repository into a single, high-quality text file called a "digest." This digest is optimized for use with chat-based LLMs like ChatGPT, enabling users to analyze and summarize repository contents efficiently.

Here's a [example](./examples//HirotoShioi_repo-digest-tool_digest.txt) of what a digest file look like on this repository.

### Purpose

The tool is designed to enable users to:

- Understand the structure and content of large codebases quickly.
- Generate high-quality summaries for documentation and analysis.
- Provide compressed repository files that can be easily processed by LLMs.

### Key Features

- **Repository Compression**: Converts all relevant files in a repository into a single text file, making it easy to process with LLMs.
- **Filtering for Quality**: Users can filter out unnecessary files to ensure the digest contains only the most relevant information. Filters can exclude CI/CD files, binary files, and more, ensuring optimal content for analysis.
- **Enhanced Summarization**: Uses built-in summary functions to produce higher-quality outputs compared to other tools.
- **HTML Reports**: Automatically generates detailed HTML reports summarizing the repository structure and key metrics.

### Use Cases for Digest Files

The generated digest files have a wide range of applications when used with LLMs:

- **Code Understanding**: Developers can quickly gain insights into large codebases without manually exploring files.
- **Documentation Generation**: Use the digest as input to create structured documentation, including API references, module overviews, or user guides.
- **Technical Debt Analysis**: Analyze the structure of a repository to identify areas with potential technical debt, such as outdated files or redundant code.
- **Team Onboarding**: Provide new team members with a high-level summary of the repository to accelerate onboarding.
- **Custom Queries**: Leverage LLMs to ask complex questions about the repository, such as "What are the key algorithms used in this codebase?" or "Which files handle authentication?"
- **Improved Debugging**: Quickly pinpoint files related to specific functionality or errors by referencing the digest.

---

## How to Use the Tool

### Prerequisites

Before setting up the tool, ensure you have the following installed on your system:

- **Node.js**: Version 18.x or higher
- **pnpm**: Preferred over npm for managing frontend dependencies
- **Docker**: For running the backend as a container

#### Setting Up

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/repo-digest-tool.git
   cd repo-digest-tool
   ```

2. **Backend and Frontend Setup**:

Use the included `makefile` for setup and management:

- Build the Docker image for the backend:
  ```bash
  make docker-build
  ```
- Start the backend container:
  ```bash
  make docker-up
  ```
- Navigate to the frontend directory and start the development server:
  ```bash
  cd frontend
  pnpm install
  pnpm run dev
  ```
- Access the API documentation at `http://localhost:8000/docs` and the frontend at `http://localhost:5173`.

### Generating a Digest

1. Navigate to a repository's details page in the frontend.
2. Click **Get Digest** to compress the repository into a single text file.
3. Use filtering options to refine the digest by excluding irrelevant files (e.g., `.log`, `.config`, or CI/CD files).
4. Download the digest file or view the HTML report to explore repository insights.

---

This guide will continue to evolve as the tool develops further. If you have feedback or feature requests, please feel free to contribute or raise an issue on the GitHub repository.
