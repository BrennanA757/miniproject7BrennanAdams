"""
Name: Brennan Adams
Class: Advanced Programming with Python
Project: Mini Project 7 - MCP Server
"""

import os
import requests
import sys
from fastmcp import FastMCP
from fastmcp.tools import tool

mcp = FastMCP("practice-hub")

BASE = os.environ.get("PRACTICE_API_URL")
TOKEN = os.environ.get("PRACTICE_API_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


class PracticeHubClient:
    def __init__(self, base_url, token):
        self.base = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {token}"}

    def print_status_error(self, status_code: int):
        if (status_code == 401):
            print(
                "401 Error: Token is missing or invalid. Please resubmit the token into environment variables.", file=sys.stderr)
        elif (status_code == 404):
            print("404 Error: Post does not exist.", file=sys.stderr)
        elif (status_code == 403):
            print("403 Error: Attempting to edit someone else's post.",
                  file=sys.stderr)
        elif (status_code == 422):
            print("422 Error: Field is either missing or is too short. Please ensure that all parameters are valid.", file=sys.stderr)

    @tool
    def create_post(self, title, body="", tags=None):
        """Create a new post on Practice Hub"""
        try:
            resp = requests.post(f"{self.base}/api/v1/posts", headers=self.headers,
                                 json={"title": title, "body": body, "tags": tags or []})
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                status = e.response.status_code
                self.print_status_error(status)
            return None

        return resp.json()

    @tool
    def list_posts(self, mine=False, tag=None):
        """List all of the posts under this profile."""
        params = {"mine": mine}
        if tag:
            params["tag"] = tag

        try:
            resp = requests.get(f"{self.base}/api/v1/posts",
                                headers=self.headers, params=params)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                status = e.response.status_code
                self.print_status_error(status)
            return None

        return resp.json()

    @tool
    def get_post(self, post_id: int):
        """GETs a post by ID"""
        try:
            resp = requests.get(
                f"{self.base}/api/v1/posts/{post_id}", headers=self.headers)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                status = e.response.status_code
                self.print_status_error(status)
            return None
        return resp.json()

    @tool
    def update_post(self, post_id: int, body: str):
        """UPDATEs a post by ID"""
        try:
            post = requests.patch(
                f"{self.base}/api/v1/posts/{post_id}", headers=self.headers, json={"body": body})
            post.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                status = e.response.status_code
                self.print_status_error(status)
            return None

        return post.json()

    @tool
    def delete_post(self, post_id: int) -> bool:
        """DELETEs a post by ID"""
        try:
            resp = requests.delete(f"{self.base}/api/v1/posts/{post_id}",
                                   headers=self.headers)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                status = e.response.status_code
                self.print_status_error(status)
            return False
        return True


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit(
            "PRACTICE_API_TOKEN is not set - see 'Set your token' in Week 2.")

    client = PracticeHubClient(BASE, TOKEN)

    # Claude code
    for method in (client.create_post, client.list_posts, client.get_post,
                   client.update_post, client.delete_post):
        mcp.add_tool(method)
    mcp.run()
    # /Claude
