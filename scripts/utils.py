import sys
import time
from datetime import datetime

from wcwidth import wcswidth


class Colors:
    """ANSI颜色代码"""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"
    GRAY = "\033[90m"


class Logger:
    """美观的日志输出类"""

    def __init__(self):
        self.start_time = time.time()

        self.completed_tasks = 0
        self.errors = 0
        self.warnings = 0

    def header(self, msg: str):
        """显示标题"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}╔{'═' * (wcswidth(msg) + 2)}╗{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}║ {msg} ║{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚{'═' * (wcswidth(msg) + 2)}╝{Colors.END}")

    def section(self, msg: str):
        """显示章节标题"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}▶ {msg}{Colors.END}")

    def success(self, msg: str):
        """显示成功信息"""
        print(f"{Colors.GREEN}✓ {msg}{Colors.END}")
        self.completed_tasks += 1

    def info(self, msg: str):
        """显示信息"""
        print(f"{Colors.CYAN}ℹ {msg}{Colors.END}")

    def warning(self, msg: str):
        """显示警告"""
        print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")
        self.warnings += 1

    def error(self, msg: str):
        """显示错误"""
        print(f"{Colors.RED}✗ {msg}{Colors.END}", file=sys.stderr)
        self.errors += 1

    def progress(self, current: int, total: int, msg: str = ""):
        """显示进度条"""
        percent = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current // total)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)

        if msg:
            print(f"\r{Colors.CYAN}[{bar}] {percent:.1f}% - {msg}{Colors.END}", end="")
        else:
            print(f"\r{Colors.CYAN}[{bar}] {percent:.1f}%{Colors.END}", end="")

        if current == total:
            print()

    def step(self, step_num: int, total_steps: int, msg: str):
        """显示步骤"""
        print(f"{Colors.BOLD}{Colors.BLUE}[{step_num}/{total_steps}]{Colors.END} {msg}")

    def divider(self, char: str = "─", length: int = 60):
        """显示分隔线"""
        print(f"{Colors.GRAY}{char * length}{Colors.END}")

    def timestamp(self, msg: str = ""):
        """显示带时间戳的消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if msg:
            print(f"{Colors.GRAY}[{timestamp}]{Colors.END} {msg}")
        else:
            print(f"{Colors.GRAY}[{timestamp}]{Colors.END}")


# 创建全局日志实例
log = Logger()
