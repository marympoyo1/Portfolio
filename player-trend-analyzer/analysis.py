from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

CORE_STATS = ["PTS", "REB", "AST"]


@dataclass
class TrendSnapshot:
    season: pd.Series
    last_five: pd.Series
    last_ten: pd.Series
    home: pd.Series
    away: pd.Series


def build_snapshot(game_log: pd.DataFrame) -> TrendSnapshot:
    if game_log.empty:
        raise ValueError("Game log is empty.")

    home_games = game_log[game_log["MATCHUP"].str.contains("vs\\.", regex=True, na=False)]
    away_games = game_log[game_log["MATCHUP"].str.contains("@", regex=False, na=False)]

    return TrendSnapshot(
        season=_round_series(game_log[CORE_STATS].mean()),
        last_five=_round_series(game_log.head(5)[CORE_STATS].mean()),
        last_ten=_round_series(game_log.head(10)[CORE_STATS].mean()),
        home=_round_series(home_games[CORE_STATS].mean()),
        away=_round_series(away_games[CORE_STATS].mean()),
    )


def build_trend_summary(snapshot: TrendSnapshot) -> list[str]:
    lines: list[str] = []

    lines.append(_compare_recent_to_season("points", snapshot.last_five["PTS"], snapshot.season["PTS"]))
    lines.append(_compare_recent_to_season("rebounds", snapshot.last_five["REB"], snapshot.season["REB"]))
    lines.append(_compare_recent_to_season("assists", snapshot.last_five["AST"], snapshot.season["AST"]))
    lines.append(_compare_home_away(snapshot.home["PTS"], snapshot.away["PTS"]))

    return lines


def format_snapshot_table(snapshot: TrendSnapshot) -> str:
    rows = {
        "Season Avg": snapshot.season,
        "Last 5": snapshot.last_five,
        "Last 10": snapshot.last_ten,
        "Home": snapshot.home,
        "Away": snapshot.away,
    }
    frame = pd.DataFrame(rows).T
    return frame.to_string()


def snapshot_rows(snapshot: TrendSnapshot) -> list[dict[str, float | str]]:
    return [
        {"label": "Season Avg", "PTS": snapshot.season["PTS"], "REB": snapshot.season["REB"], "AST": snapshot.season["AST"]},
        {"label": "Last 5", "PTS": snapshot.last_five["PTS"], "REB": snapshot.last_five["REB"], "AST": snapshot.last_five["AST"]},
        {"label": "Last 10", "PTS": snapshot.last_ten["PTS"], "REB": snapshot.last_ten["REB"], "AST": snapshot.last_ten["AST"]},
        {"label": "Home", "PTS": snapshot.home["PTS"], "REB": snapshot.home["REB"], "AST": snapshot.home["AST"]},
        {"label": "Away", "PTS": snapshot.away["PTS"], "REB": snapshot.away["REB"], "AST": snapshot.away["AST"]},
    ]


def _round_series(series: pd.Series) -> pd.Series:
    return series.fillna(0).round(1)


def _compare_recent_to_season(stat_name: str, recent: float, season: float) -> str:
    difference = round(recent - season, 1)

    if difference > 1:
        return f"Recent {stat_name} are trending up: last 5 = {recent} vs season = {season}."
    if difference < -1:
        return f"Recent {stat_name} are trending down: last 5 = {recent} vs season = {season}."

    return f"Recent {stat_name} are steady: last 5 = {recent} vs season = {season}."


def _compare_home_away(home_points: float, away_points: float) -> str:
    difference = round(home_points - away_points, 1)

    if difference > 1:
        return f"Scoring has been stronger at home: {home_points} PPG at home vs {away_points} away."
    if difference < -1:
        return f"Scoring has been stronger away from home: {away_points} PPG away vs {home_points} at home."

    return f"Home and away scoring are similar: {home_points} at home vs {away_points} away."
