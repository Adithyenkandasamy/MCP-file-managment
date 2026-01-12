from mcp.server.fastmcp import FastMCP
import os
import time
from pathlib import Path
from typing import List, Dict

# Initialize FastMCP server
mcp = FastMCP("mcp-file-server")

# Constants
# Constants
BASE_DIR = Path("/home")
def get_safe_path(path: str) -> Path:
    """
    Resolves a path to an absolute path.
    """
    # Resolve the path against the current working directory
    return Path(path).resolve()

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
    Searches from the current working directory.
    
    Args:
        keyword: String to search for in filenames.
    """
    try:
        matches = []
        # Search from current working directory to avoid scanning the entire drive
        search_base = Path(".").resolve()
        for item in search_base.rglob("*"):
            if keyword.lower() in item.name.lower():
                matches.append(str(item))
        return matches if matches else ["No matches found."]
    except Exception as e:
        return [f"Error searching files: {str(e)}"]

if __name__ == "__main__":
    # Initialize the server
    # FastMCP handles the run loop and stdio transport by default when run() is called
    mcp.run()
