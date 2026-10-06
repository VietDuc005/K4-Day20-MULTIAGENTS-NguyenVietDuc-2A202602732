### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: glob
{"path": "workspace", "pattern": "**/*"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-311.pyc', '/workspace/bookings/__pycache__/billing.cpython-311.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-311.pyc', '/workspace/bookings/__pycache__/schedule.cpython-311.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-311.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-311-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: glob
{"pattern": "*"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-311.pyc', '/workspace/bookings/__pycache__/billing.cpython-311.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-311.pyc', '/workspace/bookings/__pycache__/schedule.cpython-311.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-311.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-311-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: glob
{"pattern": ".*", "path": "workspace"}

### Tool result
No files found

### Tool call: glob
{"pattern": ".*"}

### Tool result
No files found

### Tool call: read_file
{"file_path": "workspace/README.md"}

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool call: grep
{"pattern": "Acme"}

### Tool result
No matches found

### Tool call: execute
{"command": "python -m pytest workspace/tests -q"}

### Tool result
[stderr] Traceback (most recent call last):
[stderr]   File "D:\Duc_Ky_6\VinUni\K4-Day20-MULTIAGENTS-NguyenVietDuc-2A202602732\.venv\Lib\site-packages\anyio\_core\_eventloop.py", line 204, in get_async_backend
[stderr]     return loaded_backends[asynclib_name]
[stderr]            ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
[stderr] KeyError: 'asyncio'
[stderr] 
[stderr] During handling of the above exception, another exception occurred:
[stderr] 
[stderr] Traceback (most recent call last):
[stderr]   File "<frozen runpy>", line 198, in _run_module_as_main
[stderr]   File "<frozen runpy>", line 88, in _run_code
[stderr]   File "D:\Duc_Ky_6\VinUni\K4-Day20-MULTIAGENTS-NguyenVietDuc-2A202602732\.venv\Lib\site-packages\pytest\__main__.py", line 9, in <module>
[stderr]     raise SystemExit(_console_main())
[stderr]                      ^^^^^^^^^^^^^^^
[stderr]   File "D:\Duc_Ky_6\VinUni\K4-Day20-MULTIAGENTS-NguyenVietDuc-2A202602732\.venv\Lib\site-packages\_pytest\config\__init__.py", line 253, in _console_main
[stderr]     code = _main(prog=_get_prog_name(sys.argv))
[stderr]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "D:\Duc_Ky_6\VinUni\K4-Day20-MULTIAGENTS-NguyenVietDuc-2A202602732\.venv\Lib\site-packages\_pytest\config\__init__.py", line 223, in _main
[stderr]     config = _prepareconfig(new_args, plugins, prog=prog)
[stderr]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "D:\Duc_Ky_6\VinUni\K4-Day20-MULTIAGENTS-NguyenVietDuc-2A202602732\.venv

### Tool call: execute
{"command": "python -m pytest -p no:anyio workspace/tests -q"}

### Tool result
[stderr] Traceback (most recent call last):
[stderr]   File "<frozen runpy>", line 198, in _run_module_as_main
[stderr]   File "<frozen runpy>", line 88, in _run_code
[stderr]   File "D:\Duc_Ky_6\VinUni\K4-Day20-MULTIAGENTS-NguyenVietDuc-2A202602732\.venv\Lib\site-packages\pytest\__main__.py", line 9, in <module>
[stderr]     raise SystemExit(_console_main())
[stderr]                      ^^^^^^^^^^^^^^^
[stderr]   File "D:\Duc_Ky_6\VinUni\K4-Day20-MULTIAGENTS-NguyenVietDuc-2A202602732\.venv\Lib\site-packages\_pytest\config\__init__.py", line 253, in _console_main
[stderr]     code = _main(prog=_get_prog_name(sys.argv))
[stderr]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "D:\Duc_Ky_6\VinUni\K4-Day20-MULTIAGENTS-NguyenVietDuc-2A202602732\.venv\Lib\site-packages\_pytest\config\__init__.py", line 223, in _main
[stderr]     config = _prepareconfig(new_args, plugins, prog=prog)
[stderr]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "D:\Duc_Ky_6\VinUni\K4-Day20-MULTIAGENTS-NguyenVietDuc-2A202602732\.venv\Lib\site-packages\_pytest\config\__init__.py", line 410, in _prepareconfig
[stderr]     config: Config = pluginmanager.hook.pytest_cmdline_parse(
[stderr]                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "D:\Duc_Ky_6\VinUni\K4-Day20-MULTIAGENTS-NguyenVietDuc-2A202602732\.venv\Lib\site-packages\pluggy\_hooks.py", line 512, in __call__
[stderr]     return self._hookexec(self.name, self._hookimpls.copy(), kw

### Tool call: execute
{"command": "cmd /c \"set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest workspace/tests -q\""}

### Tool result
[stderr] 'cmd' is not recognized as an internal or external command,
[stderr] operable program or batch file.

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "python -c \"import os; print('hello')\""}

### Tool result
hello

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "python -c \"import os, sys, pytest; os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'; sys.exit(pytest.main(['workspace/tests']))\""}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\lab_sandbox_v4brzu5k
collected 0 items / 1 error

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\lab_sandbox_v4brzu5k\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
D:\Duc_Ky_6\VinUni\K4-Day20-MULTIAGENTS-NguyenVietDuc-2A202602732\tasks\code-eval\workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.35s ===============================

Exit code: 2
[Command failed with exit code 2]