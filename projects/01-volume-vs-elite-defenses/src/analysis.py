"""
Project 01: Volume vs. Elite Defenses
--------------------------------------
Quantifies how much each star scorer's PPG drops vs. top-5 DRtg defenses.

Outputs:
  - data/team_drtg.csv             (team defensive ratings + tiers)
  - data/game_logs_joined.csv      (every player-game, with opponent tier attached)
  - data/comparison.csv            (per-player: PPG overall vs PPG vs elite defenses)
  - data/per_tier.csv              (per-player PPG/TS% in each opponent tier)
  - figures/headline.png           (slope chart for the README)
  - figures/tiers_heatmap.png      (player x tier heatmap, colored by diff vs own PPG)
  - figures/scoring_vs_winning.png (PPG vs Win% against top-5 defenses)

Run:
    python src/analysis.py
"""

import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import leaguegamelog, leaguedashteamstats

# -------------------- CONFIG --------------------
SEASON = "2025-26"             # NBA season to analyze
MIN_PPG_OVERALL = 20.0         # threshold to count as a "star scorer"
MIN_GAMES_VS_ELITE = 10        # filter to remove small-sample noise
TOP_N_FOR_CHART = 15           # how many players to plot on the slope chart

# -------------------- PATHS --------------------
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(HERE)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
FIG_DIR = os.path.join(PROJECT_DIR, "figures")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


def fetch_team_drtg(season: str) -> pd.DataFrame:
    """Pull team defensive ratings and assign tier buckets."""
    print(f"[1/4] Fetching team defensive ratings for {season}...")
    df = leaguedashteamstats.LeagueDashTeamStats(
        season=season,
        measure_type_detailed_defense="Advanced",
        per_mode_detailed="PerGame",
    ).get_data_frames()[0]

    drtg = df[["TEAM_ID", "TEAM_NAME", "DEF_RATING"]].copy()
    drtg["DRTG_RANK"] = drtg["DEF_RATING"].rank(method="min").astype(int)

    def tier(rank: int) -> str:
        if rank <= 5:
            return "Elite (1-5)"
        if rank <= 15:
            return "Good (6-15)"
        if rank <= 20:
            return "Average (16-20)"
        return "Poor (21-30)"

    drtg["TIER"] = drtg["DRTG_RANK"].apply(tier)
    drtg = drtg.sort_values("DRTG_RANK").reset_index(drop=True)
    drtg.to_csv(os.path.join(DATA_DIR, "team_drtg.csv"), index=False)
    print(f"      {len(drtg)} teams saved -> data/team_drtg.csv")
    return drtg


def fetch_game_logs(season: str) -> pd.DataFrame:
    """Pull every player game log for the season."""
    print(f"[2/4] Fetching player game logs for {season} (30-60s)...")
    df = leaguegamelog.LeagueGameLog(
        season=season,
        player_or_team_abbreviation="P",
    ).get_data_frames()[0]
    print(f"      {len(df):,} player-game rows pulled")
    return df


def attach_opponent_tier(logs: pd.DataFrame, drtg: pd.DataFrame) -> pd.DataFrame:
    """Parse the MATCHUP column to find opponent, then join with DRtg tiers."""
    print("[3/4] Joining games to opponent DRtg tiers...")

    # Build abbreviation -> team_id map from the game log itself
    abbr_to_id = dict(zip(logs["TEAM_ABBREVIATION"], logs["TEAM_ID"]))

    # MATCHUP is like "LAL vs. BOS" (home) or "LAL @ BOS" (away).
    # The opponent abbreviation is always the last token.
    logs = logs.copy()
    logs["OPP_ABBR"] = logs["MATCHUP"].str.split().str[-1]
    logs["OPP_TEAM_ID"] = logs["OPP_ABBR"].map(abbr_to_id)

    joined = logs.merge(
        drtg[["TEAM_ID", "TEAM_NAME", "DEF_RATING", "DRTG_RANK", "TIER"]].rename(
            columns={"TEAM_ID": "OPP_TEAM_ID",
                     "TEAM_NAME": "OPP_TEAM_NAME",
                     "DEF_RATING": "OPP_DEF_RATING",
                     "DRTG_RANK": "OPP_DRTG_RANK",
                     "TIER": "OPP_TIER"}
        ),
        on="OPP_TEAM_ID",
        how="left",
    )

    # True Shooting % per game: PTS / (2 * (FGA + 0.44 * FTA))
    joined["TS_DENOM"] = 2 * (joined["FGA"] + 0.44 * joined["FTA"])
    joined["TS_PCT"] = joined["PTS"] / joined["TS_DENOM"].replace(0, pd.NA)

    joined.to_csv(os.path.join(DATA_DIR, "game_logs_joined.csv"), index=False)
    print(f"      saved -> data/game_logs_joined.csv ({len(joined):,} rows)")
    return joined


def build_comparison(games: pd.DataFrame) -> pd.DataFrame:
    """Per player: overall PPG, PPG vs elite defenses, drop."""
    overall = games.groupby(["PLAYER_ID", "PLAYER_NAME"]).agg(
        GAMES_ALL=("GAME_ID", "count"),
        PPG_ALL=("PTS", "mean"),
        TOTAL_PTS_ALL=("PTS", "sum"),
        TOTAL_TS_DENOM_ALL=("TS_DENOM", "sum"),
    ).reset_index()
    overall["TS_PCT_ALL"] = overall["TOTAL_PTS_ALL"] / overall["TOTAL_TS_DENOM_ALL"]

    elite = games[games["OPP_TIER"] == "Elite (1-5)"].groupby(
        ["PLAYER_ID", "PLAYER_NAME"]
    ).agg(
        GAMES_ELITE=("GAME_ID", "count"),
        PPG_ELITE=("PTS", "mean"),
        TOTAL_PTS_ELITE=("PTS", "sum"),
        TOTAL_TS_DENOM_ELITE=("TS_DENOM", "sum"),
    ).reset_index()
    elite["TS_PCT_ELITE"] = elite["TOTAL_PTS_ELITE"] / elite["TOTAL_TS_DENOM_ELITE"]

    comp = overall.merge(elite, on=["PLAYER_ID", "PLAYER_NAME"], how="inner")
    comp["PPG_DROP"] = comp["PPG_ALL"] - comp["PPG_ELITE"]
    comp["PCT_DROP"] = (comp["PPG_DROP"] / comp["PPG_ALL"]) * 100

    # Star scorers only, with enough games vs elite defenses
    stars = comp[
        (comp["PPG_ALL"] >= MIN_PPG_OVERALL)
        & (comp["GAMES_ELITE"] >= MIN_GAMES_VS_ELITE)
    ].sort_values("PPG_ALL", ascending=False).reset_index(drop=True)

    keep = [
        "PLAYER_NAME", "GAMES_ALL", "GAMES_ELITE",
        "PPG_ALL", "PPG_ELITE", "PPG_DROP", "PCT_DROP",
        "TS_PCT_ALL", "TS_PCT_ELITE",
    ]
    stars[keep].to_csv(os.path.join(DATA_DIR, "comparison.csv"), index=False)
    print(f"      {len(stars)} qualifying star scorers -> data/comparison.csv")
    return stars


def build_slope_chart(stars: pd.DataFrame) -> None:
    """Slope chart: PPG all opponents -> PPG vs top-5 DRtg defenses.

    Labels on the right side are de-collided so every name is readable, even
    when multiple players land at the same PPG_ELITE value. When a label has
    been nudged off its true y-position, we draw a faint connector line back
    to the data point so the reader can match them up.
    """
    print("[4/4] Building the slope chart...")
    top = stars.head(TOP_N_FOR_CHART).copy().reset_index(drop=True)
    top["COLOR"] = top["PPG_DROP"].apply(
        lambda d: "#c0392b" if d >= 3 else "#2c7fb8"
    )

    # Taller figure gives labels more room
    fig, ax = plt.subplots(figsize=(13, 10))
    x_left, x_right = 0, 1

    # 1. Draw the slope lines + dots
    for _, row in top.iterrows():
        ax.plot(
            [x_left, x_right],
            [row["PPG_ALL"], row["PPG_ELITE"]],
            "-o",
            color=row["COLOR"],
            linewidth=2,
            markersize=7,
            alpha=0.85,
        )

    # 2. De-collide the right-side labels.
    # Sort by actual PPG_ELITE (top-to-bottom). If a label is too close to
    # the one above it, push it down by MIN_SPACING.
    labels = top.sort_values("PPG_ELITE", ascending=False).reset_index(drop=True)
    label_y = labels["PPG_ELITE"].astype(float).tolist()
    MIN_SPACING = 0.55  # minimum vertical gap between labels, in PPG units

    # Top-down pass: ensure each label is at least MIN_SPACING below the previous
    for i in range(1, len(label_y)):
        if label_y[i - 1] - label_y[i] < MIN_SPACING:
            label_y[i] = label_y[i - 1] - MIN_SPACING

    # Optional bottom-up pass if anything was pushed below the chart's range
    y_floor = labels["PPG_ELITE"].min() - 1.0
    for i in range(len(label_y) - 2, -1, -1):
        if label_y[i] - label_y[i + 1] < MIN_SPACING and label_y[i + 1] >= y_floor:
            # don't bother pushing up — top-down pass already enforced
            pass

    # 3. Draw the labels (with connector lines if nudged)
    x_label = x_right + 0.05
    for i, row in labels.iterrows():
        true_y = row["PPG_ELITE"]
        lbl_y = label_y[i]

        if abs(lbl_y - true_y) > 0.05:
            ax.plot(
                [x_right, x_label - 0.01],
                [true_y, lbl_y],
                "-",
                color=row["COLOR"],
                linewidth=0.5,
                alpha=0.45,
            )

        ax.annotate(
            f'{row["PLAYER_NAME"]}  ({row["PPG_ALL"]:.1f} → {row["PPG_ELITE"]:.1f})',
            xy=(x_label, lbl_y),
            va="center",
            fontsize=10,
            color=row["COLOR"],
        )

    ax.set_xlim(-0.15, 1.7)
    ax.set_xticks([x_left, x_right])
    ax.set_xticklabels(["vs All Opponents", "vs Top-5 DRtg"], fontsize=11)
    ax.set_ylabel("Points Per Game", fontsize=11)
    ax.set_title(
        f"Volume vs Elite Defenses ({SEASON})\n"
        f"PPG drop for {len(top)} star scorers ({MIN_PPG_OVERALL:.0f}+ PPG, "
        f"{MIN_GAMES_VS_ELITE}+ games vs elite)",
        fontsize=13,
        loc="left",
    )
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out_path = os.path.join(FIG_DIR, "headline.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"      saved -> figures/headline.png")


def build_per_tier_table(games: pd.DataFrame, star_names: list) -> pd.DataFrame:
    """For each star player, compute PPG and TS% within each opponent tier."""
    star_games = games[games["PLAYER_NAME"].isin(star_names)].copy()
    agg = star_games.groupby(["PLAYER_NAME", "OPP_TIER"]).agg(
        GAMES=("GAME_ID", "count"),
        PPG=("PTS", "mean"),
        TOTAL_PTS=("PTS", "sum"),
        TOTAL_TS_DENOM=("TS_DENOM", "sum"),
    ).reset_index()
    agg["TS_PCT"] = agg["TOTAL_PTS"] / agg["TOTAL_TS_DENOM"]
    agg.to_csv(os.path.join(DATA_DIR, "per_tier.csv"), index=False)
    return agg


def build_heatmap(per_tier: pd.DataFrame, stars: pd.DataFrame, star_names_ordered: list) -> None:
    """Player × Tier heatmap.

    Rows: top star scorers (sorted by season PPG).
    Cols: opponent tier (Elite / Good / Average / Poor).
    Cell value (text): PPG in that tier.
    Cell color: difference from the player's own season PPG.
      red = scored below their average (defender slowed them down)
      blue = scored above their average (better matchup for them)

    Coloring by diff (not raw PPG) lets you compare a 32-PPG superstar and a
    21-PPG scorer fairly — the question is "how much does each one swing",
    not "who scores more."
    """
    print("[5/6] Building player x tier heatmap...")
    tier_order = ["Elite (1-5)", "Good (6-15)", "Average (16-20)", "Poor (21-30)"]
    tier_labels = ["Elite\n(top 5)", "Good\n(6-15)", "Average\n(16-20)", "Poor\n(21-30)"]

    n = min(len(star_names_ordered), 15)
    names = star_names_ordered[:n]

    # Build a (player x tier) matrix of PPG and diff-from-own-PPG
    overall_ppg = dict(zip(stars["PLAYER_NAME"], stars["PPG_ALL"]))

    ppg_matrix = []  # raw PPG values for text labels
    diff_matrix = []  # diff from each player's own PPG (for color)
    for name in names:
        player_df = per_tier[per_tier["PLAYER_NAME"] == name].set_index("OPP_TIER")
        own_ppg = overall_ppg.get(name, 0.0)
        ppg_row = []
        diff_row = []
        for t in tier_order:
            if t in player_df.index and player_df.loc[t, "GAMES"] > 0:
                v = float(player_df.loc[t, "PPG"])
                ppg_row.append(v)
                diff_row.append(v - own_ppg)
            else:
                ppg_row.append(float("nan"))
                diff_row.append(float("nan"))
        ppg_matrix.append(ppg_row)
        diff_matrix.append(diff_row)

    import numpy as np
    ppg_arr = np.array(ppg_matrix)
    diff_arr = np.array(diff_matrix)

    # Diverging colormap centered at 0 (no change vs own PPG)
    vmax = max(abs(np.nanmin(diff_arr)), abs(np.nanmax(diff_arr)), 5.0)

    fig, ax = plt.subplots(figsize=(9, max(6, n * 0.45)))
    im = ax.imshow(diff_arr, cmap="RdBu", vmin=-vmax, vmax=vmax, aspect="auto")

    # Tick labels
    ax.set_xticks(range(len(tier_order)))
    ax.set_xticklabels(tier_labels, fontsize=10)
    ax.set_yticks(range(n))
    ax.set_yticklabels(names, fontsize=10)
    ax.tick_params(axis="x", top=True, bottom=False, labeltop=True, labelbottom=False)

    # Cell text: PPG value
    for i in range(n):
        for j in range(len(tier_order)):
            v = ppg_arr[i, j]
            if not np.isnan(v):
                # Pick text color that contrasts with cell
                cell_intensity = abs(diff_arr[i, j]) / vmax
                text_color = "white" if cell_intensity > 0.55 else "black"
                ax.text(j, i, f"{v:.1f}", ha="center", va="center",
                        fontsize=10, color=text_color, fontweight="bold")

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("PPG vs tier  −  Season PPG\n(blue = scored above own avg, red = below)",
                   fontsize=9)
    cbar.ax.tick_params(labelsize=9)

    ax.set_title(
        f"How each star's PPG shifts by opponent defense tier ({SEASON})\n"
        f"Numbers in cells = actual PPG. Color = diff from that player's season PPG.",
        fontsize=11, loc="left", pad=18,
    )
    ax.set_xlabel("")

    # Hide outer spines, keep grid effect via cell borders
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks(np.arange(len(tier_order)) - 0.5, minor=True)
    ax.set_yticks(np.arange(n) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)

    out_path = os.path.join(FIG_DIR, "tiers_heatmap.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"      saved -> figures/tiers_heatmap.png")


def build_win_scatter(games: pd.DataFrame, stars: pd.DataFrame) -> None:
    """Scatter: PPG vs elite defenses (x) vs Win% vs elite defenses (y).

    For each star scorer, restricts to games played against top-5 defenses,
    then plots:
      x = their PPG in those games
      y = their team's win % in those games
      dot size = season PPG (so high-volume scorers are visually bigger)
      color = TS% in those elite-defense games (efficiency)

    Quadrant lines at the medians split the chart into four reading zones:
      top-right    = scoring AND winning vs elite (playoff-ready)
      bottom-right = scoring but losing (empty-calorie volume)
      top-left     = winning without your star scoring (good team carrying them)
      bottom-left  = neither scoring nor winning
    """
    print("[6/6] Building scoring vs winning scatter...")

    # Restrict to games vs elite defenses, only for our qualifying stars
    star_ids = set(stars["PLAYER_ID"])
    elite_games = games[
        (games["OPP_TIER"] == "Elite (1-5)")
        & (games["PLAYER_ID"].isin(star_ids))
    ].copy()

    # Make sure we have WL as 0/1
    elite_games["WIN"] = (elite_games["WL"] == "W").astype(int)

    agg = elite_games.groupby(["PLAYER_ID", "PLAYER_NAME"]).agg(
        GAMES=("GAME_ID", "count"),
        PPG_ELITE=("PTS", "mean"),
        WIN_PCT=("WIN", "mean"),
        TOTAL_PTS=("PTS", "sum"),
        TOTAL_TS_DENOM=("TS_DENOM", "sum"),
    ).reset_index()
    agg["TS_ELITE"] = agg["TOTAL_PTS"] / agg["TOTAL_TS_DENOM"]
    agg["WIN_PCT_PCT"] = agg["WIN_PCT"] * 100

    # Bring in season PPG for dot sizing
    agg = agg.merge(stars[["PLAYER_ID", "PPG_ALL"]], on="PLAYER_ID", how="left")

    fig, ax = plt.subplots(figsize=(13, 9))

    # Dot size: scaled from season PPG (20-35 PPG range -> 100-600 marker size)
    sizes = ((agg["PPG_ALL"] - 18) * 35).clip(lower=80)

    # Color by TS% in elite games — use a viridis-ish ramp
    ts_min, ts_max = max(0.45, agg["TS_ELITE"].min()), min(0.70, agg["TS_ELITE"].max())
    cmap = plt.get_cmap("viridis")
    ts_norm = (agg["TS_ELITE"].clip(ts_min, ts_max) - ts_min) / max(ts_max - ts_min, 0.01)
    colors = [cmap(float(v)) for v in ts_norm.fillna(0.5)]

    ax.scatter(
        agg["PPG_ELITE"], agg["WIN_PCT_PCT"],
        s=sizes, c=colors, alpha=0.85,
        edgecolors="black", linewidths=0.9,
    )

    # Quadrant lines at the medians
    median_x = agg["PPG_ELITE"].median()
    median_y = agg["WIN_PCT_PCT"].median()
    ax.axvline(median_x, linestyle="--", color="gray", linewidth=0.8, alpha=0.6)
    ax.axhline(median_y, linestyle="--", color="gray", linewidth=0.8, alpha=0.6)

    # Quadrant labels in the corners
    xmin, xmax = agg["PPG_ELITE"].min() - 1.5, agg["PPG_ELITE"].max() + 2.5
    ymin, ymax = max(0, agg["WIN_PCT_PCT"].min() - 8), min(100, agg["WIN_PCT_PCT"].max() + 8)
    ax.text(xmax - 0.3, ymax - 1, "Scoring AND winning\n(playoff-ready)",
            fontsize=9, color="gray", ha="right", va="top", style="italic")
    ax.text(xmax - 0.3, ymin + 1, "Scoring but losing\n(empty-calorie volume)",
            fontsize=9, color="gray", ha="right", va="bottom", style="italic")
    ax.text(xmin + 0.3, ymax - 1, "Winning without your\nstar scoring",
            fontsize=9, color="gray", ha="left", va="top", style="italic")
    ax.text(xmin + 0.3, ymin + 1, "Neither scoring\nnor winning",
            fontsize=9, color="gray", ha="left", va="bottom", style="italic")

    # Label every star with collision avoidance
    sorted_agg = agg.sort_values("PPG_ELITE", ascending=False).reset_index(drop=True)
    placed = []
    for _, row in sorted_agg.iterrows():
        px, py = float(row["PPG_ELITE"]), float(row["WIN_PCT_PCT"])
        dx, dy = 0.25, 1.5
        lx, ly = px + dx, py + dy
        attempts = 0
        while any(abs(lx - x) < 1.8 and abs(ly - y) < 3.5 for x, y in placed) and attempts < 10:
            ly += 2.8
            attempts += 1
        placed.append((lx, ly))
        if ly - (py + dy) > 0.5:
            ax.plot([px, lx - 0.05], [py, ly], "-",
                    color="gray", linewidth=0.4, alpha=0.5, zorder=0)
        ax.annotate(row["PLAYER_NAME"], xy=(lx, ly), fontsize=8.5, va="center")

    ax.set_xlabel("PPG against Top-5 Defenses", fontsize=11)
    ax.set_ylabel("Team Win % in those games", fontsize=11)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_title(
        f"Scoring vs Winning Against Elite Defenses ({SEASON})\n"
        f"Dot size = season PPG (volume). Color = TS% in elite-defense games (efficiency, darker = lower).",
        fontsize=12, loc="left",
    )
    ax.grid(linestyle=":", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # TS% color reference
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize
    sm = ScalarMappable(norm=Normalize(vmin=ts_min, vmax=ts_max), cmap=cmap)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label("TS% vs Elite", fontsize=9)
    cbar.ax.tick_params(labelsize=9)

    out_path = os.path.join(FIG_DIR, "scoring_vs_winning.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"      saved -> figures/scoring_vs_winning.png")


def main() -> None:
    drtg = fetch_team_drtg(SEASON)
    time.sleep(1)  # be nice to the API
    logs = fetch_game_logs(SEASON)
    time.sleep(1)
    joined = attach_opponent_tier(logs, drtg)
    stars = build_comparison(joined)
    build_slope_chart(stars)

    # Order players by overall PPG for the heatmap and scatter
    star_names_ordered = stars.sort_values("PPG_ALL", ascending=False)["PLAYER_NAME"].tolist()
    per_tier = build_per_tier_table(joined, star_names_ordered)
    build_heatmap(per_tier, stars, star_names_ordered)
    build_win_scatter(joined, stars)

    print("\n=== TOP 10 BIGGEST DROPS vs ELITE DEFENSES ===")
    biggest = stars.sort_values("PPG_DROP", ascending=False).head(10)
    print(biggest[["PLAYER_NAME", "PPG_ALL", "PPG_ELITE", "PPG_DROP"]].to_string(index=False))

    print("\n=== TOP 10 MOST CONSISTENT (smallest drop) ===")
    steady = stars.sort_values("PPG_DROP").head(10)
    print(steady[["PLAYER_NAME", "PPG_ALL", "PPG_ELITE", "PPG_DROP"]].to_string(index=False))

    print("\nDone. Check:")
    print("  figures/headline.png            (slope chart)")
    print("  figures/tiers_heatmap.png       (player x tier heatmap)")
    print("  figures/scoring_vs_winning.png  (PPG vs Win% against top-5 defenses)")
    print("  data/comparison.csv             (the answer table)")
    print("  data/per_tier.csv               (per-tier breakdown for every star)")


if __name__ == "__main__":
    main()
