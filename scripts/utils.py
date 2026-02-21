import sys
import time
from datetime import datetime
from typing import Callable

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
        self.task_count = 0
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

    def task(self, msg: str, status: str = "pending"):
        """显示任务状态"""
        if status == "pending":
            print(f"{Colors.GRAY}○ {msg}{Colors.END}")
        elif status == "running":
            print(f"{Colors.CYAN}↻ {msg}{Colors.END}")
        elif status == "success":
            print(f"{Colors.GREEN}✓ {msg}{Colors.END}")
            self.completed_tasks += 1
        elif status == "failed":
            print(f"{Colors.RED}✗ {msg}{Colors.END}")
            self.errors += 1
        elif status == "warning":
            print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")
            self.warnings += 1

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

    def time_taken(self):
        """显示总耗时"""
        elapsed = time.time() - self.start_time
        if elapsed < 60:
            time_str = f"{elapsed:.2f}秒"
        else:
            minutes = int(elapsed // 60)
            seconds = elapsed % 60
            time_str = f"{minutes}分{seconds:.2f}秒"

        print(f"\n{Colors.BOLD}总耗时: {time_str}{Colors.END}")

    def summary(self):
        """显示构建摘要"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}构建摘要:{Colors.END}")
        self.divider("─", 40)
        print(f"{Colors.GREEN}✓ 完成的任务: {self.completed_tasks}{Colors.END}")
        if self.warnings > 0:
            print(f"{Colors.YELLOW}⚠ 警告: {self.warnings}{Colors.END}")
        if self.errors > 0:
            print(f"  {Colors.RED}✗ 错误: {self.errors} 个{Colors.END}")
        self.time_taken()

        if self.errors > 0:
            return False
        return True


# 创建全局日志实例
log = Logger()


# 向后兼容的函数
def info(msg: str):
    """向后兼容的info函数"""
    log.info(msg)


def err(msg: str):
    """向后兼容的err函数"""
    log.error(msg)


def greenPrint(msg: str):
    """向后兼容的greenPrint函数"""
    print(f"{Colors.GREEN}{msg}{Colors.END}")


def redPrint(msg: str):
    """向后兼容的redPrint函数"""
    print(f"{Colors.RED}{msg}{Colors.END}")


def with_spinner(func: Callable, message: str = "处理中..."):
    """带旋转指示器的函数装饰器"""
    import itertools
    import threading

    def spinner():
        spinner_chars = itertools.cycle(
            ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        )
        while not done:
            sys.stdout.write(
                f"\r{Colors.CYAN}{next(spinner_chars)} {message}{Colors.END}"
            )
            sys.stdout.flush()
            time.sleep(0.1)

    done = False
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    try:
        result = func()
    finally:
        done = True
        spinner_thread.join()
        sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")
        sys.stdout.flush()

    return result
