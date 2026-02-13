# Blog

一个菜鸟记录技术学习的仓库

## 项目结构

- assets 全局资源文件
- posts 由typst生成的博客文件，与posts_typst目录结构保持一致
- posts_typst 原始的typst文件，与posts目录结构保持一致
- scripts python的模块文件
- build.py 构建脚本，用于生成博客文件，将posts_typst生成posts
- build_out.py 用于生抽out目录以及文件，生成的文件是必要的静态文件，方便静态上传部署
- index.html 首页，用于展示博客列表等内容
- pyproject.toml 项目配置文件，用于管理项目依赖和配置信息
- README.md 说明文档，用于展示项目信息等内容
- uv.lock 项目依赖锁定文件，用于管理项目依赖版本和配置信息
