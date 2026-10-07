# 芋圆CC书源发布页

这个仓库是一个“书源发布页”，用于给 Legado / 阅读类应用一键导入书源。

## 主要文件

- **index.html**：网页首页
- **all.json**：汇总的全部书源数据
- **01.json ~ 69.json**：分批书源文件
- **cover.png、icon.png**：页面图片资源
- **renamed_sources/**：按 `bookSourceName` 自动生成的命名副本
- **source_rename_map.json**：编号文件到重命名文件的映射表

## 功能特性

- 展示各类书源
- 支持搜索和分类筛选
- 提供一键导入、复制链接、二维码导入
- 提供安全重命名方案，保留原始编号文件不丢失

## 自动改名方案

仓库新增了批量重命名脚本，避免直接覆盖原始编号文件导致回滚困难。

运行方式：

```bash
python scripts/rename_sources.py
```

脚本会：

- 读取每个编号文件里的 `bookSourceName`
- 生成更易识别的文件名
- 将重命名后的副本复制到 `renamed_sources/`
- 生成 `source_rename_map.json` 映射表

这样既能保留原始 `01.json`、`02.json` 等文件，又能生成一套按书源名命名的可用版本。

## 使用方式

访问 [书源发布页](https://yuyuan-cc.github.io/shuyuan/) 直接导入或复制链接。
