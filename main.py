"""main."""

import re
from pathlib import Path

import nbformat
from nbconvert import MarkdownExporter


def convert_and_merge(notebook_paths: list[str], output_md: str) -> None:
    markdown_exporter = MarkdownExporter()
    full_content = []

    for nb_path in notebook_paths:
        # Читаем ноутбук
        with Path(nb_path).open("r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # Конвертируем в Markdown
        (body, resources) = markdown_exporter.from_notebook_node(notebook)
        body_cleaned = re.sub(r"<style scoped>.*?</style>", "", body, flags=re.DOTALL)
        # # Добавляем заголовок с именем файла (опционально)
        # full_content.append(f"\n\n# {nb_path}\n\n")
        full_content.append(body_cleaned)

    # Сохраняем объединённый файл
    with Path(output_md).open("w", encoding="utf-8") as f:
        # with open(output_md, "w", encoding="utf-8") as f:
        f.write("\n".join(full_content))


if __name__ == "__main__":
    notebooks = [
        "jupyter_notebooks/header.ipynb",
        "jupyter_notebooks/examples.ipynb",
    ]

    convert_and_merge(notebooks, "README.md")
