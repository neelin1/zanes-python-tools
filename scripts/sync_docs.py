#!/usr/bin/env python3
import shutil

def sync_docs():
    """Copies the content of CLAUDE.md to AGENTS.md and GEMINI.md."""
    source_file = 'CLAUDE.md'
    destination_files = ['AGENTS.md', 'GEMINI.md']

    for dest_file in destination_files:
        try:
            shutil.copyfile(source_file, dest_file)
            print(f"Successfully copied {source_file} to {dest_file}")
        except IOError as e:
            print(f"Error copying file: {e}")
            exit(1)

if __name__ == "__main__":
    sync_docs()
