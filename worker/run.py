import argparse
import sys
import time
from datetime import UTC, datetime
from pathlib import Path


BACKEND_PATH = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_PATH))

from app.database import SessionLocal, create_db_tables
from app.fetch_service import run_fetch_cycle


def _log(message: str) -> None:
    timestamp = datetime.now(UTC).isoformat()
    print(f"[{timestamp}] {message}", flush=True)


def run_once() -> None:
    create_db_tables()

    with SessionLocal() as db:
        result = run_fetch_cycle(db)

    _log(
        "fetch completed: "
        f"sources={result['sources']} "
        f"fetched={result['fetched_articles']} "
        f"saved={result['saved_articles']} "
        f"errors={len(result['errors'])}"
    )

    for error in result["errors"]:
        _log(f"source error: {error}")


def run_loop(interval_seconds: int) -> None:
    _log(f"worker started with interval_seconds={interval_seconds}")

    while True:
        try:
            run_once()
        except Exception as error:
            _log(f"fetch failed: {error}")

        time.sleep(interval_seconds)


def main() -> None:
    parser = argparse.ArgumentParser(description="fe-brief RSS worker")
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Run continuously instead of executing one fetch cycle.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=3600,
        help="Seconds between fetch cycles when --loop is enabled.",
    )
    args = parser.parse_args()

    if args.loop:
        run_loop(args.interval)
    else:
        run_once()


if __name__ == "__main__":
    main()
