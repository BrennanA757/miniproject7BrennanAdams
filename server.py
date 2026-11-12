"""
Name: Brennan Adams
Class: Advanced Programming with Python
Project: Mini Project 7 - MCP Server
"""

import os
import requests
from fastmcp import FastMCP

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
                "401 Error: Token is missing or invalid. Please resubmit the token into environment variables.")
        elif (status_code == 404):
            print("404 Error: Post does not exist.")
        elif (status_code == 403):
            print("403 Error: Attempting to edit someone else's post.")
        elif (status_code == 422):
            print("422 Error: Field is either missing or is too short. Please ensure that all parameters are valid.")

    @mcp.tool()
    def create_post(self, title, body="", tags=None):
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

    @mcp.tool()
    def list_posts(self, mine=False, tag=None):
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

    @mcp.tool()
    def get_post(self, post_id: int):
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

    @mcp.tool()
    def update_post(self, post_id: int, body: str):
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

    @mcp.tool()
    def delete_post(self, post_id: int) -> bool:
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

    new_post = client.create_post("Test Post", "test")
    if (new_post != None):
        post_id = new_post["id"]
        post = client.get_post(post_id)
        print(f"Successfully created post {post}")

        client.update_post(post_id, "updated text")
        post = client.get_post(post_id)
        print(f"Successfully updated post {post}")

        client.delete_post(post_id)
        print("Deleted newly created post")
