# GitHub MCP Server · 让 AI 原生操作 GitHub

> 与其手动点 GitHub 网页，不如让 AI 直接帮你管 PR、Issue、代码搜索

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude%20Code-4B61FF?logo=anthropic)](https://claude.com)
[![Platform: Cursor](https://img.shields.io/badge/Platform-Cursor-7B42FF?logo=cursor)](https://cursor.com)
[![Platform: VS Code](https://img.shields.io/badge/Platform-VS%20Code-007ACC?logo=visual-studio-code)](https://code.visualstudio.com)

---

## 中文 | [English](#english)

### 这是什么？

一个让 AI Agent **原生操作 GitHub** 的 MCP Server。

不用切换浏览器，不用手动点网页。直接告诉 AI 你想做什么，它帮你完成。

### 问题

```
你日常做的事                AI 帮你做的事
─────────────────────────────────────────────────
"帮我找这个仓库的 PR"       → 直接列出 PR 列表
"创建个 Issue"             → 自动创建，还带模板
"搜一下这段代码在哪"        → 直接返回文件位置
```

**问题在哪？**

> AI 不知道你是谁，不知道你的仓库，更没法替你操作 GitHub。

所以 AI 只能"建议"你做什么，而不是"替"你做什么。

### 解决

```python
# 用自然语言操作 GitHub
search_repos("mcp server python")     # 搜索仓库
get_pr_details("owner", "repo", 123)  # 查看 PR
create_issue("owner", "repo", "Bug: xxx", "复现步骤...")  # 创建 Issue
list_issues("owner", "repo", "open")  # 列出 Issues
search_code("def main()")             # 搜索代码
```

### 支持的工具

| 工具 | 功能 |
|------|------|
| `search_repos` | 搜索 GitHub 仓库 |
| `get_pr_details` | 获取 PR 详情 |
| `create_issue` | 创建 Issue |
| `list_issues` | 列出仓库 Issues |
| `search_code` | 全局搜索代码 |

### 快速开始

#### 1. 安装依赖

```bash
pip install mcp httpx
```

#### 2. 配置 GitHub Token（推荐）

```bash
# 创建一个 Personal Access Token:
# GitHub → Settings → Developer settings → Personal access tokens → Generate new token
# 勾选 repo 权限

export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

> 不配置 Token 也可以用，但速率限制更低（60次/小时 vs 5000次/小时）

#### 3. 在 Claude Code 中使用

```bash
# 添加到 ~/.claude/settings.local.json
```

```json
{
  "mcpServers": {
    "github": {
      "command": "python",
      "args": ["/path/to/github_mcp.py"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### 4. 开始对话

```bash
# 启动 Claude Code 后，直接说：
"帮我看看这个仓库最近有哪些 open 的 PR"
"创建一个 Bug report，标题是 xxx"
"搜索一下项目中有没有 TODO"
```

---

### 使用示例

#### 搜索仓库
```
"帮我找一下 GitHub 上流行的 MCP server"
AI → search_repos("mcp server") → 返回仓库列表
```

#### 查看 PR
```
"PR #456 改了什么？"
AI → get_pr_details("owner", "repo", 456) → 返回 PR 内容
```

#### 创建 Issue
```
"帮我在这个仓库创建一个 Bug report"
AI → 询问你 Bug 描述 → create_issue(...) → Issue 创建成功
```

---

### 适用场景

- 🤖 **AI Agent 开发** - 让 AI 原生操作 GitHub
- 🔍 **代码审查** - AI 自动搜索和分析代码
- 📋 **Issue 管理** - 自动创建、更新、管理 Issue
- 🔄 **自动化工作流** - 结合其他 MCP Server 实现复杂自动化

---

### Rate Limits

| 类型 | 无 Token | 有 Token |
|------|----------|----------|
| 搜索 | 10 次/分 | 30 次/分 |
| 其他 | 60 次/时 | 5000 次/时 |

---

### 技术栈

- Python 3.10+
- [FastMCP](https://modelcontextprotocol.io/) - MCP 框架
- httpx - 异步 HTTP 客户端
- GitHub REST API

---

### License

MIT

---

## English

An MCP server for GitHub operations - enables AI agents to manage PRs, issues, and search code via natural language.

### Features

- `search_repos` - Search GitHub repositories
- `get_pr_details` - Get PR information
- `create_issue` - Create a new issue
- `list_issues` - List issues in a repository
- `search_code` - Search code across GitHub

### Quick Start

```bash
pip install mcp httpx
export GITHUB_TOKEN="your_token"
python github_mcp.py
```

Add to your Claude Code config and start chatting!
