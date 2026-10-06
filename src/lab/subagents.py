"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use when you need to explore the codebase, inspect directory structure, read README, "
                "docstrings, schemas, raw data, or log samples without modifying any files. "
                "The explorer returns a factual investigation report."
            ),
            "system_prompt": (
                "You are an exploration subagent. Your role is strictly read-only: inspect files, read docstrings, "
                "and analyze logs or schemas. Provide a clear, concise, and factual summary of your findings. "
                "Do not create or edit any files."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when you need to execute code changes, write output files, run data cleaning routines, "
                "or run Python commands and tests to verify fixes. "
                "Provide all necessary context, requirements, and file paths."
            ),
            "system_prompt": (
                "You are an implementation subagent. Your role is to perform specific file creations, code edits, "
                "data processing, or run tests via the shell as requested by the main agent. "
                "Report exactly what changes were made and the outcome of any verification commands."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use when work has been implemented and you need an independent audit of the workspace against "
                "the task requirements, edge cases, output file formats, and constraints. "
                "The reviewer checks results without making changes."
            ),
            "system_prompt": (
                "You are a quality assurance reviewer subagent. Your role is strictly read-only: verify that all "
                "required output files exist, match expected schemas, column names, formats, and pass tests. "
                "Highlight any discrepancies, missing requirements, or edge cases."
            ),
        },
    ]
