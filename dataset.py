"""Read the local title;summary; rows produced by crawler.py."""

from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent / "plot_summaries.txt"


def load_documents(path: Path = DATA_PATH) -> list[tuple[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(
            f"{path.name} is missing. Run crawler.py when permitted, "
            "or provide a dataset you are allowed to use in the same format."
        )

    documents = []
    for line in path.read_text(encoding="utf-8").splitlines():
        title, separator, remainder = line.partition(";")
        if not separator:
            continue

        summary = remainder[:-1] if remainder.endswith(";") else remainder
        title = title.strip()
        summary = summary.strip()
        if title and summary:
            documents.append((title, summary))

    if not documents:
        raise ValueError(f"No valid title/summary rows were found in {path.name}.")

    return documents
