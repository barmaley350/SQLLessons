"""main."""

import re
from pathlib import Path

import nbformat
from nbconvert import MarkdownExporter


def convert_and_merge(notebook_paths: list[str], output_md: str) -> None:
    """Convert notebooks to markdown and merge them."""
    markdown_exporter = MarkdownExporter()
    full_content = []

    for nb_path in notebook_paths:
        with Path(nb_path).open("r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        (body, resources) = markdown_exporter.from_notebook_node(notebook)  # noqa: RUF059
        body_cleaned = re.sub(r"<style scoped>.*?</style>", "", body, flags=re.DOTALL)
        full_content.append(body_cleaned)

    with Path(output_md).open("w", encoding="utf-8") as f:
        f.write("\n".join(full_content))


if __name__ == "__main__":
    notebooks = [
        "jupyter_notebooks/header.ipynb",
        "jupyter_notebooks/examples.ipynb",
    ]

    convert_and_merge(notebooks, "README.md")
