# MCP Local File Saver

A Python-based MCP server for Claude Desktop that lets you save, append, read, and list local text notes.

## Features

- Save a note as a local `.txt` file
- Append new content to an existing note
- Append Claude’s response to a note
- Read a note by title
- List all saved notes
- Expose saved notes through an MCP resource
- Summarize note content with an MCP prompt

## Built With

- Python
- MCP Python SDK
- Claude Desktop
- `uv`

## Project Structure

```bash
mcp-local-file-saver/
├── main.py
├── .gitignore
├── pyproject.toml
├── uv.lock
└── notes/   # ignored from git
```

## MCP Capabilities

### Tools

- `save_note(title, content)`
- `append_note(title, content)`
- `append_response_to_note(note_name, response_text)`
- `read_note(title)`
- `list_notes()`

### Resources

- `notes://all`

### Prompts

- `summarize_note(...)`

## Example Use Cases

You can ask Claude things like:

- Save this response to `mcp-learning`
- Append that answer to `oracle-notes`
- Read my `fav players` note
- List all my saved notes
- Summarize my `interview prep` note

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd mcp-local-file-saver
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Run locally with MCP Inspector

```bash
uv run mcp dev main.py
```

### 4. Run with Claude Desktop

Add the server to your Claude Desktop config using your local Python interpreter inside `.venv`.

Example:

```json
{
  "mcpServers": {
    "Local File Saver": {
      "command": "/absolute/path/to/project/.venv/bin/python",
      "args": [
        "/absolute/path/to/project/main.py"
      ]
    }
  }
}
```

## Notes

- Notes are stored locally in the `notes/` folder
- The `notes/` folder is ignored in git
- The server runs over `stdio`

## Why I Built This

I built this project to get hands-on experience with MCP by creating a practical local productivity tool. It helped me understand how MCP tools, resources, and prompts work together in a real Claude Desktop integration.

## Future Improvements

- Support Apple Pages
- Support Google Docs
- Search notes by keyword
- Read notes by exact filename
- Add tags or metadata to notes
- Add better summarization workflows

## License

MIT

