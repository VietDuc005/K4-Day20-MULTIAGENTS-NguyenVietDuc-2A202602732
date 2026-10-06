---
name: error-handling
description: Use when encountering file-related errors during task execution, especially when files are expected to be present.
---
# Error Handling for Missing Files

1. **Verify File Paths**: Ensure that the file paths specified in your code are correct and accessible. Check for typos or incorrect directory structures.
2. **Check File Existence**: Before attempting to read or write files, implement checks to confirm that the files exist using functions like `os.path.exists()`.
3. **Handle Exceptions**: Use try-except blocks around file operations to gracefully handle `FileNotFoundError` and provide informative error messages.
4. **Log Errors**: Log the error details to help diagnose issues later. Include the file path and the operation that failed.
5. **Create Missing Files**: If your task requires certain files to exist, implement logic to create them if they are missing, or provide clear instructions on how to generate them.
6. **Use Temporary Directories**: When working with temporary files, ensure that the paths are correctly set up to avoid conflicts with existing files or directories.
7. **Test in Isolation**: Run file operations in isolation to ensure they work as expected before integrating them into larger workflows.