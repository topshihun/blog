import shutil
import subprocess
import sys
import time
from pathlib import Path

import minify_html

from scripts.check import check_dependencies
from scripts.utils import Colors, log


class BlogBuilder:
    """博客构建器"""

    def __init__(self):
        self.start_time = time.time()
        self.total_posts = 0
        self.compiled_posts = 0
        self.minified_files = 0
        self.errors = 0

    def show_banner(self):
        """显示构建横幅"""
        log.header("博客构建系统")
        log.timestamp(f"开始构建: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        log.divider()

    def clean_output(self):
        """清理输出目录"""
        log.section("清理输出目录")

        out_dir = Path("out")
        if out_dir.exists():
            try:
                shutil.rmtree(out_dir)
                log.success(f"已删除目录: {out_dir}")
            except Exception as e:
                log.error(f"删除目录失败: {e}")
                return False
        else:
            log.info("输出目录不存在，无需清理")

        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            log.success(f"已创建目录: {out_dir}")
        except Exception as e:
            log.error(f"创建目录失败: {e}")
            return False

        return True

    def count_posts(self):
        """统计Typst文章数量"""
        posts_dir = Path("posts")
        if not posts_dir.exists():
            log.warning("posts目录不存在")
            return 0

        typ_files = list(posts_dir.rglob("*.typ"))
        self.total_posts = len(typ_files)
        log.info(f"找到 {self.total_posts} 个Typst文件")
        return self.total_posts

    def compile_posts(self):
        """编译所有Typst文章"""
        if self.total_posts == 0:
            log.warning("没有找到要编译的文章")
            return True

        log.section("编译文章")
        log.step(1, 3, f"编译 {self.total_posts} 篇文章")

        posts_dir = Path("posts")
        out_dir = Path("out/posts")

        for i, typ_file in enumerate(posts_dir.rglob("*.typ"), 1):
            relative_path = typ_file.relative_to(posts_dir)
            html_file = out_dir / relative_path.with_suffix(".html")

            # 创建输出目录
            html_file.parent.mkdir(parents=True, exist_ok=True)

            # 显示进度
            log.progress(i, self.total_posts, f"编译: {relative_path}")

            # 编译命令
            command = [
                "typst",
                "compile",
                "--features",
                "html",
                "--format",
                "html",
                str(typ_file),
                str(html_file),
            ]

            try:
                subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.compiled_posts += 1
                log.timestamp(f"完成: {relative_path}")
            except subprocess.CalledProcessError as e:
                log.error(f"编译失败: {relative_path}")
                log.error(f"错误信息: {e.stderr.strip() if e.stderr else '未知错误'}")
                self.errors += 1
                return False
            except Exception as e:
                log.error(f"编译异常: {relative_path} - {str(e)}")
                self.errors += 1
                return False

        log.success(f"成功编译 {self.compiled_posts}/{self.total_posts} 篇文章")
        return True

    def copy_static_files(self):
        """复制静态文件"""
        log.section("复制静态文件")
        log.step(2, 3, "复制静态资源")

        static_files = {
            "assets": "目录",
            "index.html": "文件",
            "favicon.ico": "文件",
            "robots.txt": "文件",
        }

        for item, item_type in static_files.items():
            src = Path(item)
            dst = Path("out") / item

            if not src.exists():
                log.warning(f"{item_type}不存在: {item}")
                continue

            try:
                if src.is_dir():
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

                log.success(f"已复制: {item}")
            except Exception as e:
                log.error(f"复制失败: {item} - {str(e)}")
                self.errors += 1

        return True

    def minify_html_files(self):
        """压缩HTML文件"""
        log.section("压缩文件")
        log.step(3, 3, "压缩HTML和JS文件")

        # 压缩HTML文件
        html_files = list(Path("out").rglob("*.html"))
        if html_files:
            log.info(f"找到 {len(html_files)} 个HTML文件需要压缩")

            for i, html_file in enumerate(html_files, 1):
                log.progress(
                    i, len(html_files), f"压缩HTML: {html_file.relative_to('out')}"
                )

                try:
                    with open(html_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    minified = minify_html.minify(content)

                    with open(html_file, "w", encoding="utf-8") as f:
                        f.write(minified)

                    self.minified_files += 1
                except Exception as e:
                    log.error(f"HTML压缩失败: {html_file} - {str(e)}")
                    self.errors += 1

            log.success(f"已压缩 {self.minified_files} 个HTML文件")

        # 压缩JS文件
        js_files = list(Path("out").rglob("*.js"))
        if js_files:
            log.info(f"找到 {len(js_files)} 个JS文件需要压缩")

            for i, js_file in enumerate(js_files, 1):
                log.progress(i, len(js_files), f"压缩JS: {js_file.relative_to('out')}")

                try:
                    subprocess.run(
                        ["terser", str(js_file), "-o", str(js_file)],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    self.minified_files += 1
                except subprocess.CalledProcessError as e:
                    log.error(f"JS压缩失败: {js_file}")
                    log.error(
                        f"错误信息: {e.stderr.strip() if e.stderr else '未知错误'}"
                    )
                    self.errors += 1
                except Exception as e:
                    log.error(f"JS压缩异常: {js_file} - {str(e)}")
                    self.errors += 1

            log.success(f"已压缩 {len(js_files)} 个JS文件")

        return True

    def show_summary(self):
        """显示构建摘要"""
        log.header("构建完成")

        elapsed = time.time() - self.start_time
        if elapsed < 60:
            time_str = f"{elapsed:.2f}秒"
        else:
            minutes = int(elapsed // 60)
            seconds = elapsed % 60
            time_str = f"{minutes}分{seconds:.2f}秒"

        print()
        log.divider("═", 50)
        print(f"{Colors.BOLD}{Colors.CYAN}📊 构建统计:{Colors.END}")
        log.divider("─", 50)

        # 文章编译统计
        if self.total_posts > 0:
            status_color = (
                Colors.GREEN
                if self.compiled_posts == self.total_posts
                else Colors.YELLOW
            )
            print(f"{Colors.BOLD}文章编译:{Colors.END}")
            print(
                f"  {status_color}✓ 成功: {self.compiled_posts}/{self.total_posts}{Colors.END}"
            )
            if self.compiled_posts < self.total_posts:
                print(
                    f"  {Colors.YELLOW}⚠ 失败: {self.total_posts - self.compiled_posts}{Colors.END}"
                )

        # 文件压缩统计
        if self.minified_files > 0:
            print(f"{Colors.BOLD}文件压缩:{Colors.END}")
            print(f"  {Colors.GREEN}✓ 已压缩: {self.minified_files} 个文件{Colors.END}")

        # 错误统计
        if self.errors > 0:
            print(f"{Colors.BOLD}错误统计:{Colors.END}")
            print(f"  {Colors.RED}✗ 错误: {self.errors} 个{Colors.END}")
        else:
            print(f"{Colors.BOLD}错误统计:{Colors.END}")
            print(f"  {Colors.GREEN}✓ 无错误{Colors.END}")

        log.divider("─", 50)
        print(f"{Colors.BOLD}⏱️  总耗时: {time_str}{Colors.END}")
        log.divider("═", 50)

        if self.errors > 0:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ 构建完成，但有错误{Colors.END}")
            return False
        else:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ 构建成功完成！{Colors.END}")
            return True

    def build(self):
        """执行完整的构建流程"""
        self.show_banner()

        # 检查依赖
        log.section("初始化检查")
        if not check_dependencies():
            log.error("依赖检查失败，构建中止")
            return False

        # 清理输出目录
        if not self.clean_output():
            log.error("清理输出目录失败，构建中止")
            return False

        # 统计文章
        self.count_posts()

        # 编译文章
        if not self.compile_posts():
            log.error("文章编译失败，构建中止")
            return False

        # 复制静态文件
        if not self.copy_static_files():
            log.warning("部分静态文件复制失败，继续构建")

        # 压缩文件
        if not self.minify_html_files():
            log.warning("部分文件压缩失败，继续构建")

        # 显示摘要
        return self.show_summary()


def main():
    """主函数"""
    try:
        builder = BlogBuilder()
        success = builder.build()

        if not success:
            sys.exit(1)

    except KeyboardInterrupt:
        log.error("\n构建被用户中断")
        sys.exit(1)
    except Exception as e:
        log.error(f"构建过程中发生未预期的错误: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
