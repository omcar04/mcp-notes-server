from pathlib import Path
import re

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Local File Saver")

BASE_DIR = Path(__file__).resolve().parent
NOTES_DIR = BASE_DIR / "notes"
NOTES_DIR.mkdir(exist_ok=True)


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled"

def note_path_from_title(title: str) -> Path:
    return NOTES_DIR / f"{slugify(title)}.txt"

@mcp.tool()
def save_note(title: str, content: str) -> str:
    """Save a note to a local text file."""
    if not title.strip():
        raise ValueError("Title cannot be empty")
    if not content.strip():
        raise ValueError("Content cannot be empty")

    filename = f"{slugify(title)}.txt"
    filepath = NOTES_DIR / filename

    filepath.write_text(content.strip() + "\n", encoding="utf-8")
    return f"Saved note to {filepath}"


@mcp.tool()
def append_note(title: str, content: str) -> str:
    """Append content to an existing note. Fails if the note does not exist."""
    if not title.strip():
        raise ValueError("Title cannot be empty")
    if not content.strip():
        raise ValueError("Content cannot be empty")

    filepath = note_path_from_title(title)

    if not filepath.exists():
        raise FileNotFoundError(
            f"No existing note found for title '{title}'. "
            f"Check notes://all for available files first."
        )

    with filepath.open("a", encoding="utf-8") as f:
        f.write("\n" + content.strip() + "\n")

    return f"Appended content to {filepath}"

@mcp.tool()
def append_response_to_note(note_name: str, response_text: str) -> str:
    """Append Claude's response text to an existing note."""
    return append_note(title=note_name, content=response_text)

@mcp.tool()
def read_note_by_filename(filename: str) -> str:
    """Read a note by exact filename. Use notes://all to find the filename first."""
    if not filename.strip():
        raise ValueError("filename cannot be empty")

    safe_name = filename.strip()
    if not safe_name.endswith(".txt"):
        safe_name += ".txt"

    filepath = NOTES_DIR / safe_name

    if not filepath.exists():
        raise FileNotFoundError(f"No note found with filename '{safe_name}'")

    return filepath.read_text(encoding="utf-8")

@mcp.tool()
def list_notes() -> str:
    """List all .txt files in the notes directory."""
    files = sorted(NOTES_DIR.glob("*.txt"))

    if not files:
        return "No notes found."

    return "\n".join(file.name for file in files)

@mcp.resource("notes://all")
def list_all_notes() -> str:
    """List all .txt files in the notes directory."""
    files = sorted(NOTES_DIR.glob("*.txt"))

    if not files:
        return "No notes found."

    return "\n".join(file.name for file in files)


@mcp.prompt()
def summarize_note(title: str, note_text: str) -> str:
    """Create a prompt for summarizing a saved note."""
    return f"""
Summarize the following note titled "{title}".

Please provide:
1. A short summary
2. Key points
3. Action items, if any
4. Important names, topics, or decisions mentioned

Keep the response clear and concise.

Note content:
{note_text}
""".strip()

if __name__ == "__main__":
    mcp.run(transport="stdio")