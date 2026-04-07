# GitHub MCP Server Specification

## Overview
MCP Server for GitHub operations - enables AI agents to manage PRs, issues, and search code via natural language.

## Features

### Tools
1. `search_repos` - Search GitHub repositories
2. `get_pr_details` - Get PR information
3. `create_issue` - Create a new issue
4. `list_issues` - List issues in a repository
5. `search_code` - Search code across repositories

## Technical Stack
- Python 3.10+
- FastMCP
- httpx (async HTTP client)
- PyGithub or direct REST API

## Implementation
Using FastMCP + httpx + GitHub REST API (no PyGithub dependency)

## Status
Implementation started - 2026-04-07
