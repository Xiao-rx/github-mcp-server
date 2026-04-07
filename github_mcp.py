"""
GitHub MCP Server
Enables AI agents to manage PRs, issues, and search code via natural language.
"""

import os
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("github")

# GitHub API base
GITHUB_API = "https://api.github.com"

# Get token from environment
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def _get_headers() -> dict:
    """Get headers for GitHub API requests."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


@mcp.tool()
async def search_repos(query: str, per_page: int = 5) -> str:
    """
    Search GitHub repositories.

    Args:
        query: Search query (e.g., "python web framework", "mcp server")
        per_page: Number of results to return (default 5, max 100)

    Returns:
        JSON string with search results
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/search/repositories",
            headers=_get_headers(),
            params={"q": query, "per_page": per_page},
            timeout=30.0,
        )

        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        data = response.json()
        results = []
        for repo in data.get("items", []):
            results.append({
                "name": repo["full_name"],
                "description": repo.get("description", ""),
                "stars": repo["stargazers_count"],
                "language": repo.get("language", ""),
                "url": repo["html_url"],
            })

        return f"Found {data.get('total_count', 0)} repos. Top results:\n" + "\n".join(
            f"- {r['name']} ({r['stars']} stars) - {r['description'][:100]}"
            for r in results
        )


@mcp.tool()
async def get_pr_details(owner: str, repo: str, pr_number: int) -> str:
    """
    Get details of a specific pull request.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        pr_number: Pull request number

    Returns:
        JSON string with PR details
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}",
            headers=_get_headers(),
            timeout=30.0,
        )

        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        pr = response.json()
        return (
            f"PR #{pr['number']}: {pr['title']}\n"
            f"State: {pr['state']}\n"
            f"Author: {pr['user']['login']}\n"
            f"URL: {pr['html_url']}\n"
            f"Body: {pr.get('body', 'No description')[:200]}"
        )


@mcp.tool()
async def create_issue(
    owner: str,
    repo: str,
    title: str,
    body: str = "",
    labels: list[str] = None
) -> str:
    """
    Create a new issue in a repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        title: Issue title
        body: Issue description (optional)
        labels: List of label names (optional)

    Returns:
        JSON string with created issue details
    """
    async with httpx.AsyncClient() as client:
        payload: dict[str, Any] = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels

        response = await client.post(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues",
            headers=_get_headers(),
            json=payload,
            timeout=30.0,
        )

        if response.status_code != 201:
            return f"Error: {response.status_code} - {response.text}"

        issue = response.json()
        return (
            f"Created issue #{issue['number']}: {issue['title']}\n"
            f"URL: {issue['html_url']}"
        )


@mcp.tool()
async def list_issues(
    owner: str,
    repo: str,
    state: str = "open",
    per_page: int = 10
) -> str:
    """
    List issues in a repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        state: Issue state - "open", "closed", or "all" (default "open")
        per_page: Number of results to return (default 10)

    Returns:
        JSON string with list of issues
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues",
            headers=_get_headers(),
            params={"state": state, "per_page": per_page},
            timeout=30.0,
        )

        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        issues = response.json()
        if not issues:
            return f"No {state} issues found in {owner}/{repo}"

        results = []
        for issue in issues:
            if "pull_request" in issue:
                continue  # Skip PRs, only show issues
            results.append(
                f"- #{issue['number']}: {issue['title']} ({issue['state']})"
            )

        return f"{owner}/{repo} {state} issues:\n" + "\n".join(results)


@mcp.tool()
async def search_code(query: str, per_page: int = 5) -> str:
    """
    Search code across GitHub.

    Args:
        query: Search query (e.g., "def main()", "TODO: fix")
        per_page: Number of results to return (default 5)

    Returns:
        JSON string with search results
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/search/code",
            headers=_get_headers(),
            params={"q": query, "per_page": per_page},
            timeout=30.0,
        )

        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        data = response.json()
        results = []
        for item in data.get("items", [])[:per_page]:
            results.append({
                "file": item["path"],
                "repo": item["repository"]["full_name"],
                "url": item["html_url"],
            })

        return (
            f"Found {data.get('total_count', 0)} code matches.\n"
            + "\n".join(f"- {r['repo']}: {r['file']}" for r in results)
        )


if __name__ == "__main__":
    mcp.run()
