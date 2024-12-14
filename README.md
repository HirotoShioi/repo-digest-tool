# Repo Digest Tool: Features and Usage Guide

![example](./examples/ScreenShot%202024-12-15%206.58.15.png)

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

## Setup & Usage

### Prerequisites

- Docker Engine 24.0.0 or later
- Docker Compose v2.0.0 or later

### Installation & Running

1. Build the application:

```bash
make build
```

2. Start the application:

```bash
make run
```

The application will be available at:

- Frontend: `http://localhost`
- API: `http://localhost:8000`
- API Documentation: `http://localhost:8000/redoc`

### Management Commands

- Stop the application:

```bash
make down
```

- View logs:

```bash
make logs
```

- Clean up all resources:

```bash
make clean
```
