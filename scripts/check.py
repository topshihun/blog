import shutil

from scripts.utils import log

required_tools = ["terser", "typst"]


def check_dependencies():
    """检查所有必需的依赖工具"""
    log.section("检查依赖")

    all_found = True
    total_tools = len(required_tools)

    for i, tool in enumerate(required_tools, 1):
        log.progress(i, total_tools, f"检查: {tool}")

        if shutil.which(tool) is None:
            log.error(f"未找到工具: {tool}")
            all_found = False
        else:
            log.success(f"找到工具: {tool}")

    log.divider()

    if all_found:
        log.success("所有依赖检查通过")
    else:
        log.error("缺少必需的依赖工具")
        log.info("请安装以下工具:")
        for tool in required_tools:
            if shutil.which(tool) is None:
                log.info(f"  - {tool}")

    return all_found


def check_typst_version():
    """检查Typst版本"""
    import subprocess

    try:
        result = subprocess.run(
            ["typst", "--version"], capture_output=True, text=True, check=True
        )
        version = result.stdout.strip()
        log.info(f"Typst版本: {version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        log.warning("无法获取Typst版本信息")
        return False


def check_terser_version():
    """检查Terser版本"""
    import subprocess

    try:
        result = subprocess.run(
            ["terser", "--version"], capture_output=True, text=True, check=True
        )
        version = result.stdout.strip()
        log.info(f"Terser版本: {version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        log.warning("无法获取Terser版本信息")
        return False


def check_all():
    """执行所有检查"""
    log.header("系统检查")

    # 检查依赖
    deps_ok = check_dependencies()

    if deps_ok:
        # 检查版本
        log.section("检查工具版本")
        check_typst_version()
        check_terser_version()

        log.success("系统检查完成")
        return True
    else:
        log.error("系统检查失败")
        return False


if __name__ == "__main__":
    # 直接运行时的测试
    check_all()
