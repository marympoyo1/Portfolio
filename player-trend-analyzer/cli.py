from __future__ import annotations

import argparse
from datetime import date

from analysis import build_snapshot, build_trend_summary, format_snapshot_table
from api_client import fetch_player_game_log, find_player_by_name


def current_nba_season(today: date | None = None) -> str:
    today = today or date.today()
    start_year = today.year if today.month >= 10 else today.year - 1
    end_year = (start_year + 1) % 100
    return f"{start_year}-{end_year:02d}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze recent NBA player trends using NBA.com data."
    )
    parser.add_argument("--player", help="Full player name, for example 'Stephen Curry'")
    parser.add_argument(
        "--season",
        default=current_nba_season(),
        help="NBA season in YYYY-YY format, for example 2024-25",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    player_name = args.player or input("Enter an NBA player name: ").strip()

    if not player_name:
        raise SystemExit("A player name is required.")

    try:
        player = find_player_by_name(player_name)
        game_log = fetch_player_game_log(player.player_id, args.season)
        snapshot = build_snapshot(game_log)
        summary_lines = build_trend_summary(snapshot)

        print("\nPLAYER TREND ANALYZER")
        print("-" * 72)
        print(f"Player: {player.full_name}")
        print(f"Season: {args.season}")
        print(f"Games analyzed: {len(game_log)}")
        print()
        print(format_snapshot_table(snapshot))
        print("\nTrend summary")
        print("-" * 72)
        for line in summary_lines:
            print(f"- {line}")
    except Exception as error:
        raise SystemExit(f"Error: {error}") from error


if __name__ == "__main__":
    main()
