import os

# Folders we don't want to scan
EXCLUDED_DIRS = {"node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build"}

# File extensions to include (we save contents)
INCLUDED_EXTS = {
    ".js", ".ts", ".jsx", ".tsx",      # JavaScript/TypeScript
    ".html", ".css", ".scss",          # Frontend
    ".py", ".json", ".md", ".txt", 
    ".yml", ".yaml"                    # Backend / config
}

# File extensions to exclude (fonts + images + binaries)
EXCLUDED_EXTS = {
    ".ttf", ".woff", ".woff2", ".otf", ".eot",   # fonts
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".ico"  # images
}

# Specific files to exclude
EXCLUDED_FILES = {"package-lock.json"}

# Files to include explicitly (even if no extension)
INCLUDED_FILES = {"Dockerfile", "docker-compose.yml", "docker-compose.yaml"}

def save_project_to_file(output_file="code.txt"):
    root_dir = os.getcwd()  # current directory
    script_file = os.path.basename(__file__)  # this script's filename

    with open(output_file, "w", encoding="utf-8") as out:
        for folder, dirs, files in os.walk(root_dir):
            # Exclude unwanted directories
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

            for file in files:
                # Skip output file, this script, and explicitly excluded files
                if file == output_file or file == script_file or file in EXCLUDED_FILES:
                    continue  

                ext = os.path.splitext(file)[1].lower()
                file_path = os.path.join(folder, file)
                rel_path = os.path.relpath(file_path, root_dir)

                out.write(f"{rel_path}:\n")
                out.write("-" * 80 + "\n")  # separator line

                # Decide if we should include the file
                if ext in INCLUDED_EXTS or file in INCLUDED_FILES:
                    try:
                        if os.path.getsize(file_path) == 0:
                            out.write("[Empty file]")
                        else:
                            with open(file_path, "r", encoding="utf-8") as f:
                                out.write(f.read())
                    except Exception as e:
                        out.write(f"[Could not read file: {e}]")
                else:
                    out.write("[Skipped: excluded file type]")

                out.write("\n\n")  # spacing between files

    print(f"✅ All project code and file list saved to {output_file}")


if __name__ == "__main__":
    save_project_to_file()

