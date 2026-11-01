"""Single-pass Typst export for the initial Player's Book."""
import subprocess
from pathlib import Path


def export(typst, root, book):
    target = book / "output/galaxies-of-legend-players-book.pdf"
    command = [typst, "compile", "--root", str(root), "--font-path", str(book / "fonts"),
               str(book / "book.typ"), str(target)]
    subprocess.run(command, check=True)
    print(f"Exported {target.stat().st_size / 1024:.0f} KiB PDF: {target}")
