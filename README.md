### INF601 - Advanced Programming in Python

### Brennan Adams

### Mini Project 7

# Project Title

MCP Setup & Troubleshooting

## Description

Project for creating, editing, retrieving, and deleting posts at https://practice.fhsucyber.com

## Getting Started

### Dependencies

- This project needs Python3, the requests library, a valid Hub API token stored in the PRACTICE_API_TOKEN environment variable, and an OS that supports environment variables.
- Before running the program, you must first run 'pip install requests' and '$env:PRACTICE_API_TOKEN = "your token here"'.

### Installing

- Run 'git clone https://github.com/BrennanA757/miniproject7BrennanAdams.git' inside the desired directory.
- requirements.txt also includes the 'requests' library.

### Executing program

- Install the library by running 'pip install requests fastmcp'
- Set the environment variable PRACTICE_API_TOKEN by running '$env:PRACTICE_API_TOKEN = "your token here"'

## Help

- "PRACTICE_API_TOKEN is not set"
  -Run '$env:PRACTICE_API_TOKEN = "your token here"' and make sure you have a valid token.

- "401 Error - 'Token is missing or invalid'"
  -Verify the token if you haven't already
  -Re-set the environment variable
  -Close and re-open the terminal

- "404 Error - Post does not exist"
  -Use 'client.list_posts(mine=True)' to see a list of valid post IDs.
  -Ensure you are using a valid post ID.

- "403 Error - Attempting to edit someone else's post'
  -Ensure you are attempting to edit one of your posts. Client.py will not allow editing of others' posts.

- "422 Error - Field is missing or too short.
  -Ensure that the post title, body, and any required fields are all optimally set.
  -For example, 'client.create_post("My Title", body="Some content", tags=["week3"])

- "ConnectionError" or "Failed to extablish a new connection"
  -Ensure you have a strong internet connection.

- "ModuleNotFoundError: No Module named 'requests'"
  -Ensure that you have run the command 'pip install requests' before running.

## Authors

Contributors names and contact info

Brennan Adams
email: b_adams2@mail.fhsu.edu

## Version History

- 0.2
  - Edited README.md
- 0.1
  - Initial Release

## License

No License

## Acknowledgments

None

## AI Usage

I used AI for testing the code that I created, but nothing much outside of that. Anything inside 
a "# Claude Code" comment was written by Claude and was not modified by me.
