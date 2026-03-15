@echo off
chcp 65001 >nul
REM FastAPI Project Unit Test Script

echo ========================================
echo FastAPI Project Unit Test
echo ========================================
echo.

REM Change to test directory
cd /d D:\python_test\news_toutiao\toutiao_test

echo Running tests...
echo.

REM Run tests directly with full path
D:\python_test\news_toutiao\toutiao\.venv\Scripts\python.exe -m pytest test_comprehensive.py -v -s --tb=short

echo.
echo ========================================
echo Test completed!
echo ========================================
pause
