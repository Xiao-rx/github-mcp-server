# GitHub MCP Server

An MCP server for GitHub operations - enables AI agents to manage PRs, issues, and search code via natural language.

## Features

- `search_repos` - Search GitHub repositories
- `get_pr_details` - Get PR information
- `create_issue` - Create a new issue
- `list_issues` - List issues in a repository
- `search_code` - Search code across GitHub

## Installation

```bash
# Install dependencies
pip install mcp httpx

# Set GitHub token (optional but recommended for higher rate limits)
export GITHUB_TOKEN="your_github_token_here"

# Run the server
python github_mcp.py
```

## Claude Desktop Configuration

Add to `~/.claude/settings.local.json`:

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

## Usage Examples

### Search Repositories
```
Search for popular MCP servers:
"search_repos" with query="mcp server python"
```

### Get PR Details
```
Get details of PR #123 in owner/repo:
"get_pr_details" with owner="owner", repo="repo", pr_number=123
```

### Create Issue
```
Create a bug report:
"create_issue" with owner="owner", repo="repo", title="Bug: Login broken", body="Steps to reproduce..."
```

### List Issues
```
List open issues:
"list_issues" with owner="owner", repo="repo", state="open"
```

### Search Code
```
Search for TODO comments:
"search_code" with query="TODO: fix language:python"
```

## Rate Limits

- Without token: 60 requests/hour
- With token: 5,000 requests/hour

## License

MIT
