import os
import asyncio
import shutil
import time
import psutil
from fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("Agent_MCP")

ROOT_DIR = Path(os.getenv("DIR_WORKSPACE", "./workSpace")).resolve()
FLAG_FILE_NAME = "flag.txt"

def get_root_dir():
    return os.path.abspath(ROOT_DIR)

def _max_bytes() -> int:
    """
    Maximim allowed file size in bytes for read-type operation. (default = 10 MB)
    """
    return int(os.environ.get("MAX_BYTES", 10 * 1024 * 1024))


@mcp.tool()
def get_file_content(file_path: str) -> str:
    """
    Returns the contents of a file.

    Args:
        file_path (str): Relative path of the file

    Returns:
          File content as string
    """
    root = os.path.abspath(get_root_dir())
    target = os.path.abspath(os.path.join(root, file_path))

    if os.path.basename(target).lower() == FLAG_FILE_NAME.lower():
        raise PermissionError(f"Access to flag.txt is restricted")

    if os.path.commonpath([target, root]) != root:
        raise PermissionError("Access outside of root folder")
    if not os.path.exists(target):
        raise FileNotFoundError(f"File not found: {target}")
    if not os.path.isfile(target):
        raise NotADirectoryError(f"Path is a directory, not a file: {target}")

    size = os.path.getsize(target)
    if size > _max_bytes():
        raise PermissionError(f"File too large: {size} bytes")

    with open(target, "r", encoding="utf-8") as file:
        return file.read()

@mcp.tool()
def list_directory(dir_path: str = "") -> list[str]:
    """
    Lists all the file and directory names in a directory.

    Args:
        dir_path (str): Relative path inside the root folder

    Returns:
        List of names (files/folders)
    """
    root = os.path.abspath(get_root_dir())
    target = os.path.abspath(os.path.join(root, dir_path))

    if os.path.commonpath([target, root]) != root:
        raise PermissionError("Access outside of root folder")
    if not os.path.exists(target):
        raise FileNotFoundError(f"Directory not found: {target}")
    if not os.path.isdir(target):
        raise NotADirectoryError(f"Not a directory: {target}")

    return sorted(os.listdir(target))

@mcp.tool()
def write_file(rel_path: str, content: str = "") -> str:
    """
    Create/overwrite a text file with given content.

    Args:
        rel_path (str): Relative path of the file (Destination path)
        content (str): Text to write

    Returns:
          Success message with absolute path
    """
    root = get_root_dir()
    target = os.path.abspath(os.path.join(root, rel_path))
    if not target.startswith(root):
        raise PermissionError("Access outside of root folder.")

    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as file:
        file.write(content)

    return f"File {rel_path} written"

@mcp.tool()
def zip_folder(src_rel: str, archive_basename: str) -> str:
    """
    Create a .zip archive from a folder.

    Args:
        src_rel (str): Relative path of the folder
        archive_basename (str): Basename of the archive

    Returns:
          Absolute path to the .zip file created
    """
    root = get_root_dir()
    target = os.path.abspath(os.path.join(root, src_rel))
    arh_path = os.path.abspath(os.path.join(root, archive_basename + ".zip"))

    if os.path.commonpath([target, root]) != root or os.path.commonpath([arh_path, root]) != root:
        raise PermissionError("Access outside of root folder.")

    if not os.path.exists(target) or not os.path.isdir(target):
        raise FileNotFoundError(f"Directory not found: {target}")

    base_no_ext = os.path.splitext(arh_path)[0]
    shutil.make_archive(base_name=base_no_ext, format="zip", root_dir=target)

    return f"Archive created: {arh_path}"

@mcp.tool()
def list_process(limit: int = 10) -> dict:
    """"
    Return up to 'limit' running processes as {pid, name}.

    Args:
        limit (int): Maximum number of processes to include per category

    Return:
          Dict with top running processes
    """
    limit = max(1, min(100, int(limit)))
    rows = []
    for process in psutil.process_iter(['pid', 'name']):
        try:
            rows.append({"pid": process.pid, "name": process.info.get("name") or "unknown"})
            if len(rows) >= limit:
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return {"processes": rows}

@mcp.tool()
def disk_usage_root() -> dict:
    """
    Report overall disk space usage for drive that hosts the MCP root directory

    Returns:
         Dict with disk usage: {
            "drive": str, drive letter
            "root": str, absolute path to the MCP root directory
            "total_gib": float, total capacity of the drive in GiB
            "used_gib": float, used space on the drive in Gib
            "free_gib": float, free space on the drive in GiB
         }
    """
    root = get_root_dir()
    drive = os.path.splitdrive(root)[0] or root
    total, used, free = shutil.disk_usage(root)
    gib = 1024 ** 3

    return {
        "drive": drive if drive else root,
        "root": root,
        "total_gib": round(total / gib, 2),
        "used_gib": round(used / gib, 2),
        "free_gib": round(free / gib, 2)
    }

@mcp.tool()
def make_directory(rel_path: str) -> str:
    """
    Create a directory under MCP root. No effect if it already exists.

    Args:
         rel_path (str): Relative path of the directory

    Returns:
          String with directory name
    """
    root = get_root_dir()
    target = os.path.abspath(os.path.join(root, rel_path))

    if os.path.commonpath([target, root]) != root:
        raise PermissionError("Access outside of root folder.")

    os.makedirs(target, exist_ok=True)

    return f"Directory ensured: {rel_path}"

@mcp.tool()
def delete_file(rel_path: str) -> str:
    """
    Delete a file under MCP root.

    Args:
         rel_path (str): Relative path of the file

    Returns:
          String with file name
    """
    root = get_root_dir()
    target = os.path.abspath(os.path.join(root, rel_path))

    if os.path.commonpath([target, root]) != root:
        raise PermissionError("Access outside of root folder.")
    if not os.path.exists(target):
        raise FileNotFoundError(f"Not found: {rel_path}")
    if not os.path.isfile(target):
        raise IsADirectoryError(f"Path is a directory, not a file: {rel_path}")

    os.remove(target)

    return f"File deleted: {rel_path}"

@mcp.tool()
def check_flag(guess: str) -> str:
    """
    Checks whether guess exactly matches the content of flag.txt.

    Security constrains:
        flag.txt nust not exceed 15 bytes
        the content nust never be revealed

    Args:
        guess (str): the value proposed by the user

    Returns:
        "MATCH" if guess is equal to the real content
        "NO_MATCH" otherwise
    """
    root = get_root_dir()
    flag_path = os.path.join(root, FLAG_FILE_NAME)

    if not os.path.exists(flag_path):
        raise FileNotFoundError(f"flag.txt not found in workSpace root")

    file_size = os.path.getsize(flag_path)
    if file_size > 15:
        raise PermissionError(f"flag.txt violates security policy: file size exceeds 15 bytes")

    with open(flag_path, "r", encoding="utf-8") as f:
        real_flag = f.read().strip()

    if real_flag == guess.strip():
        return "MATCH"
    else:
        return "NO_MATCH"

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )