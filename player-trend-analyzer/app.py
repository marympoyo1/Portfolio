from __future__ import annotations

from datetime import date

from flask import Flask, render_template, request, send_from_directory

from analysis import build_snapshot, build_trend_summary, snapshot_rows
from api_client import fetch_player_game_log, find_player_by_name

app = Flask(__name__)


def current_nba_season(today: date | None = None) -> str:
    today = today or date.today()
    start_year = today.year if today.month >= 10 else today.year - 1
    end_year = (start_year + 1) % 100
    return f"{start_year}-{end_year:02d}"


def recent_games_rows(game_log):
    recent_games = game_log.head(5).copy()
    recent_games["GAME_DATE"] = recent_games["GAME_DATE"].dt.strftime("%b %d, %Y")
    columns = ["GAME_DATE", "MATCHUP", "WL", "PTS", "REB", "AST"]
    return recent_games[columns].to_dict(orient="records")


@app.route("/styles.css")
def styles():
    return send_from_directory("public", "styles.css")


@app.route("/", methods=["GET", "POST"])
def index():
    player_name = request.form.get("player", "").strip()
    season = request.form.get("season", current_nba_season()).strip() or current_nba_season()

    context = {
        "default_season": current_nba_season(),
        "player_name": player_name,
        "season": season,
        "report": None,
        "error": None,
    }

    if request.method == "POST":
        if not player_name:
            context["error"] = "Enter a player name to analyze recent trends."
            return render_template("index.html", **context)

        try:
            player = find_player_by_name(player_name)
            game_log = fetch_player_game_log(player.player_id, season)
            snapshot = build_snapshot(game_log)

            context["report"] = {
                "player_name": player.full_name,
                "season": season,
                "games_analyzed": len(game_log),
                "summary_lines": build_trend_summary(snapshot),
                "snapshot_rows": snapshot_rows(snapshot),
                "recent_games": recent_games_rows(game_log),
            }
        except Exception as error:
            context["error"] = str(error)

    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
