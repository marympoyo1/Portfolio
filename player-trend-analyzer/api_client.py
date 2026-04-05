from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players


@dataclass
class PlayerMatch:
    player_id: int
    full_name: str


def find_player_by_name(name: str) -> PlayerMatch:
    matches = players.find_players_by_full_name(name)
    if not matches:
        raise ValueError(f"No NBA player found for '{name}'.")

    player = matches[0]
    return PlayerMatch(player_id=player["id"], full_name=player["full_name"])


def fetch_player_game_log(player_id: int, season: str) -> pd.DataFrame:
    response = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season,
        season_type_all_star="Regular Season",
    )
    frames = response.get_data_frames()

    if not frames:
        raise ValueError("No game log data was returned.")

    game_log = frames[0].copy()
    if game_log.empty:
        raise ValueError(f"No regular-season game log data was returned for season {season}.")

    game_log["GAME_DATE"] = pd.to_datetime(game_log["GAME_DATE"])
    game_log = game_log.sort_values("GAME_DATE", ascending=False).reset_index(drop=True)
    return game_log
