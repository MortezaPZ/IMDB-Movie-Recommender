"""Build a local title/plot dataset when access is permitted by the source."""

from __future__ import annotations

import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.imdb.com"
OUTPUT_PATH = Path(__file__).resolve().parent / "plot_summaries.txt"
REQUEST_DELAY_SECONDS = 1.0
HEADERS = {
    "User-Agent": (
        "IMDbMovieRecommender/1.0 "
        "(educational project; https://github.com/MortezaPZ/IMDB-Movie-Recommender)"
    )
}
TITLE_ID = re.compile(r"^/title/(tt\d+)(?:/|$)")


def fetch_page(session: requests.Session, url: str) -> BeautifulSoup:
    response = session.get(url, timeout=(5, 20))
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).replace(";", ",").strip()


def get_top_movies(page: BeautifulSoup) -> list[tuple[str, str]]:
    movies = []
    seen_ids = set()
    for link in page.select("a.ipc-title-link-wrapper[href]"):
        match = TITLE_ID.match(link["href"])
        if not match or match.group(1) in seen_ids:
            continue
        title_id = match.group(1)
        title = clean_text(link.get_text(" ", strip=True))
        seen_ids.add(title_id)
        movies.append((title_id, title))
        if len(movies) == 250:
            break
    return movies


def get_plot_summary(page: BeautifulSoup) -> str:
    summaries = []
    for section in page.find_all(attrs={"data-testid": "sub-section-summaries"}):
        text = clean_text(section.get_text(" ", strip=True))
        if text and text not in summaries:
            summaries.append(text)
    return " ".join(summaries)


def main() -> None:
    with requests.Session() as session:
        session.headers.update(HEADERS)
        chart = fetch_page(session, urljoin(BASE_URL, "/chart/top/"))
        movies = get_top_movies(chart)
        if not movies:
            raise SystemExit("No movie links found. The source page markup may have changed.")

        saved = 0
        with OUTPUT_PATH.open("w", encoding="utf-8", newline="\n") as output:
            for index, (title_id, chart_title) in enumerate(movies, start=1):
                if index > 1:
                    time.sleep(REQUEST_DELAY_SECONDS)
                url = urljoin(BASE_URL, f"/title/{title_id}/plotsummary/")
                try:
                    page = fetch_page(session, url)
                except requests.RequestException as error:
                    status = error.response.status_code if error.response is not None else None
                    if status in {403, 429}:
                        raise SystemExit(
                            f"Source returned HTTP {status}; stopping instead of retrying."
                        ) from error
                    print(f"Skipped {title_id}: {error}")
                    continue

                heading = page.find("h1", attrs={"data-testid": "hero__pageTitle"})
                title = clean_text(heading.get_text(" ", strip=True)) if heading else chart_title
                summary = get_plot_summary(page)
                if not summary:
                    print(f"Skipped {title_id}: no plot summary was found.")
                    continue
                output.write(f"{title or title_id};{summary};\n")
                saved += 1
                print(f"[{index}/{len(movies)}] saved {title or title_id}")

    print(f"Saved {saved} summaries to {OUTPUT_PATH.name}.")


if __name__ == "__main__":
    main()
