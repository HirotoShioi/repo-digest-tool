### PoC Plan for Core Functionality in Rust

The following plan outlines the implementation of core functionalities in Rust as a PoC (Proof of Concept) to assess the feasibility of migrating from Python. The goal is to clone a repository, filter files, generate a summary, and create a compressed digest file.

---

### **Step 1: Define Core Functionalities**

1. **Essential Features**:

   - Clone a repository.
   - Filter files.
   - Generate a summary.
   - Create a compressed digest file.

2. **Crate Selection**:
   - **Git Operations**: `git2` or `gitoxide`
   - **File Operations**: `std::fs` and `walkdir`
   - **Asynchronous Processing**: `tokio`
   - **Template Engine**: `tera` (for HTML report generation)
   - **Token Calculation**: `tiktoken-rs`
   - **Compression**: `zip` or `flate2` (for ZIP compression)

---

### **Step 2: Scope of the PoC**

1. **Repository Cloning**:

   - Use the `git2` crate to clone a repository.
   - Implement error handling and logging.

2. **File Filtering**:

   - Use the `walkdir` crate to recursively traverse repository files.
   - Read `.gptignore` and `.gptinclude` files and implement filtering logic using the `globset` crate.

3. **Summary Generation**:

   - Calculate token counts using `tiktoken-rs`.
   - Collect statistics such as file count, total size, and per-extension statistics.
   - Render results into HTML format using the `tera` template engine.

4. **Compressed File Creation**:
   - Use filtered file lists and summaries to create a compressed file using the `zip` or `flate2` crate.

---

### **Step 3: Implementation Plan**

1. **Project Setup**:

   - Initialize a new Rust project and add required crates to `Cargo.toml`.

2. **Module Breakdown**:

   - `clone`: Handles repository cloning.
   - `filter`: Implements file filtering logic.
   - `summary`: Handles token calculation and summary generation.
   - `compress`: Creates the compressed digest file.

3. **Module Implementation and Testing**:

   - **`clone` Module**:
     - Clone the repository to a specified directory using `git2`.
     - Log success or failure of the operation.
   - **`filter` Module**:
     - Parse `.gptignore` and `.gptinclude` files.
     - Display filtering results for verification.
   - **`summary` Module**:
     - Calculate token counts, file sizes, and statistics.
     - Manage results using structured data and render with `tera`.
   - **`compress` Module**:
     - Combine filtered files and the summary into a single ZIP file.

4. **Integration Testing**:
   - Integrate all modules and perform end-to-end testing.
   - Use small repositories as test cases.

---

### **Step 4: Deliverables and Evaluation**

1. **Deliverables**:

   - Clone a specified repository.
   - Produce filtered file results based on `.gptignore`/`.gptinclude`.
   - Generate an HTML report with token statistics.
   - Create a ZIP file containing filtered files and the summary.

2. **Evaluation Criteria**:
   - Does Rust implementation outperform Python in terms of performance?
   - Is the code maintainable and readable?
   - Are all required features achievable in Rust?

---

### **Proposed Schedule**

| Step   | Duration |
| ------ | -------- |
| Step 1 | 1 day    |
| Step 2 | 2 days   |
| Step 3 | 5 days   |
| Step 4 | 2 days   |

---

### **Next Actions**

1. Install required crates (`git2`, `walkdir`, `globset`, `tiktoken-rs`, `tera`, `zip`).
2. Begin with the basic functionality of the `clone` module.
3. Implement a simple version of the filtering logic and validate results.

---

This PoC will clarify the feasibility and effectiveness of migrating to Rust. Feel free to share any additional requirements or questions!
