from mcp.server.fastmcp import FastMCP
import os
import time
from pathlib import Path
from typing import List, Dict

# Initialize FastMCP server
mcp = FastMCP("mcp-file-server")

# Constants
BASE_DIR = Path("./workspace").resolve()

def get_safe_path(path: str) -> Path:
    """
    Resolves a path and ensures it is within the base directory.
    Raises ValueError if the path is unsafe.
    """
    # Allow absolute paths if they are within BASE_DIR, otherwise join with BASE_DIR
    target_path = Path(path)
    if not target_path.is_absolute():
        target_path = (BASE_DIR / path).resolve()
    else:
        target_path = target_path.resolve()

    if not str(target_path).startswith(str(BASE_DIR)):
        raise ValueError(f"Access denied: Path '{path}' is outside the base directory.")
    
    return target_path

@mcp.tool()
async def list_files(directory: str = ".") -> List[str]:
    """
    List files and directories in the specified path within the workspace.
    
    Args:
        directory: Relative path to the directory (default is root of workspace).
    """
    try:
        safe_path = get_safe_path(directory)
        if not safe_path.exists():
            return [f"Error: Directory '{directory}' does not exist."]
        if not safe_path.is_dir():
            return [f"Error: '{directory}' is not a directory."]
        
        items = []
        for item in safe_path.iterdir():
            prefix = "[DIR] " if item.is_dir() else "[FILE]"
            items.append(f"{prefix} {item.name}")
        return sorted(items)
    except Exception as e:
        return [f"Error listing files: {str(e)}"]

@mcp.tool()
async def read_file(file_path: str) -> str:
    """
    Read the contents of a text file.
    
    Args:
        file_path: Relative path to the file.
    """
    try:
        safe_path = get_safe_path(file_path)
        if not safe_path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not safe_path.is_file():
            return f"Error: '{file_path}' is not a file."
        
        return safe_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "Error: File content is not valid UTF-8 text."
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
async def file_info(file_path: str) -> str:
    """
    Get metadata about a file.
    
    Args:
        file_path: Relative path to the file.
    """
    try:
        safe_path = get_safe_path(file_path)
        if not safe_path.exists():
            return f"Error: File '{file_path}' does not exist."
        
        stats = safe_path.stat()
        modified_time = time.ctime(stats.st_mtime)
        file_type = "Directory" if safe_path.is_dir() else "File"
        
        return (
            f"Path: {file_path}\n"
            f"Type: {file_type}\n"
            f"Size: {stats.st_size} bytes\n"
            f"Last Modified: {modified_time}"
        )
    except Exception as e:
        return f"Error getting file info: {str(e)}"

@mcp.tool()
async def search_files(keyword: str) -> List[str]:
    """
    Recursively search for files whose names contain the keyword.
    
    Args:
        keyword: String to search for in filenames.
    """
    try:
        matches = []
        for item in BASE_DIR.rglob("*"):
            if keyword.lower() in item.name.lower():
                # Return path relative to BASE_DIR for cleaner output
                matches.append(str(item.relative_to(BASE_DIR)))
        return matches if matches else ["No matches found."]
    except Exception as e:
        return [f"Error searching files: {str(e)}"]

if __name__ == "__main__":
    # Initialize the server
    # FastMCP handles the run loop and stdio transport by default when run() is called
    mcp.run()
