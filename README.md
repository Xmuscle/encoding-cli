# encoding-cli

`encoding-cli` 是一个基于 `uv` 的命令行工具，用于在 AI 辅助开发场景下在伪GB2312/GB18030 字节流与 UTF-8 之间转换，并提供 round-trip 校验与编码判断。

转换规则：

- `to_utf8`: 伪GB2312流 -> 按 `GB18030` 解码 -> 输出 `UTF-8`
- `to_gbk`: `UTF-8` -> 按 `GB18030` 编码 -> 输出伪GB2312流
- 当前“伪GB2312流”按原样透传处理，不做额外映射

## 安装

### 方式一：直接按项目运行

在项目目录下：

```bash
cd /i/ui_development/ui_development/cli/encoding-cli
uv run encoding-cli --help
```

或者直接指定项目路径：

```bash
uv run --project "I:/ui_development/ui_development/cli/encoding-cli" encoding-cli --help
```

### 方式二：安装到当前项目环境

```bash
cd /i/ui_development/ui_development/cli/encoding-cli
uv sync
uv run encoding-cli --help
```

### 方式三：安装为全局命令

```bash
uv tool install "I:/ui_development/ui_development/cli/encoding-cli"
encoding-cli --help
```

## 运行

```bash
uv run encoding-cli --help
uv run encoding-cli to_utf8 -i legacy.bin -o utf8.txt
uv run encoding-cli to_gbk -i utf8.txt -o legacy.bin
uv run encoding-cli verify -i legacy.bin
uv run encoding-cli is_utf8 -i utf8.txt
uv run encoding-cli is_gbk -i legacy.bin
```

## 退出码

- `0`: 成功
- `1`: 转换失败，或 `is_utf8` / `is_gbk` 判断为 false
- `2`: `verify` 校验失败

## 命令说明

### `to_utf8`

将输入字节按 `gb18030` 解码后输出为 UTF-8。失败时向 stderr 输出错误信息，并返回非 0。

### `to_gbk`

将 UTF-8 输入编码为 `gb18030` 字节并输出。失败时向 stderr 输出错误信息，并返回非 0。

### `verify`

执行完整链路校验：

`伪GB2312流 -> GB18030解码 -> UTF-8 -> GB18030编码 -> 伪GB2312流`

输出是否通过、是否可判为 UTF-8、是否可判为 GBK，以及失败原因。若输入同时兼容 UTF-8 与 GB18030（例如 ASCII），会额外输出歧义说明。

### `is_utf8` / `is_gbk`

输出 `true` 或 `false`，并在 stderr 输出判断原因。

## 开发与测试

```bash
uv run pytest
```
