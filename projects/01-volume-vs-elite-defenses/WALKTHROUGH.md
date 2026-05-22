# Click-by-click walkthrough — Project 01 (Volume vs. Elite Defenses)

**Goal of this doc:** finish Project 01 by yourself in class. Every step says exactly what to click and what to type. Expected wait times are noted in `[brackets]`. If something looks different from what's described, **stop and check the troubleshooting section at the bottom** — don't guess.

You are starting from this state (already done):
- Git and Python installed
- Repo cloned to `C:\Users\User\Documents\Claude\Projects\ANALYTICS PORTFOLIO\NBA-Analytics-Portfolio`
- Virtual environment created in `.venv`
- Packages installed (`nba_api`, `pandas`, `matplotlib`, `jupyter`)
- `src/analysis.py`, `requirements.txt`, and `writeup.md` already exist in the project folder

---

## Step 1 — Open the project in VS Code

If VS Code is already open with the repo (you should see `NBA-ANALYTICS-PORTFOLIO` in the left sidebar), skip to Step 2.

Otherwise:
1. Open VS Code.
2. **File → Open Folder…**
3. Navigate to `C:\Users\User\Documents\Claude\Projects\ANALYTICS PORTFOLIO\NBA-Analytics-Portfolio`
4. Click **Select Folder**.

You should now see `projects`, `.venv`, `.gitignore`, `LICENSE`, `README.md` in the left sidebar.

---

## Step 2 — Open the terminal

Press **`Ctrl + ` `** (the backtick key, top-left of keyboard).

A terminal panel opens at the bottom. The prompt should end with `NBA-Analytics-Portfolio>`.

---

## Step 3 — Activate the virtual environment

In the terminal, type exactly:

```
.\.venv\Scripts\Activate.ps1
```

Press Enter.

**You should see** `(.venv)` appear at the start of your prompt:

```
(.venv) PS C:\Users\User\Documents\Claude\Projects\ANALYTICS PORTFOLIO\NBA-Analytics-Portfolio>
```

If you get an error about "running scripts is disabled," see the troubleshooting section.

---

## Step 4 — Move into the project folder

In the terminal, type:

```
cd projects\01-volume-vs-elite-defenses
```

Press Enter. The prompt now ends with `...\01-volume-vs-elite-defenses>`.

---

## Step 5 — Run the analysis

This is the one big step. Type:

```
python src/analysis.py
```

Press Enter. **You'll see progress messages like:**

```
[1/4] Fetching team defensive ratings for 2024-25...
      30 teams saved -> data/team_drtg.csv
[2/4] Fetching player game logs for 2024-25 (30-60s)...
      27,000 player-game rows pulled
[3/4] Joining games to opponent DRtg tiers...
      saved -> data/game_logs_joined.csv
[4/4] Building the slope chart...
      saved -> figures/headline.png

=== TOP 10 BIGGEST DROPS vs ELITE DEFENSES ===
[a table of names with PPG numbers]

=== TOP 10 MOST CONSISTENT (smallest drop) ===
[another table]

Done. Check figures/headline.png and data/comparison.csv
```

**Expected wait:** 30-90 seconds total. The `nba_api` call to fetch game logs is the slow part. If nothing seems to happen for 2 minutes, the API might be rate-limiting — wait another minute, then if still stuck, hit `Ctrl + C` and re-run.

---

## Step 6 — Open the chart

In the VS Code left sidebar, expand `projects/01-volume-vs-elite-defenses/figures/`. Click `headline.png`. It opens in the main editor area.

You should see a slope chart with around 15 player names, with lines going from "vs All Opponents" on the left to "vs Top-5 DRtg" on the right. Red lines = big drop. Blue lines = consistent scorer.

**Quick sanity check:** the names should look like real NBA stars (e.g., names you'd recognize). If you see weird gibberish, something went wrong — check troubleshooting.

---

## Step 7 — Open the data file

In the VS Code left sidebar, expand `projects/01-volume-vs-elite-defenses/data/`. Click `comparison.csv`.

It opens as text. Look at the columns:
- `PLAYER_NAME`, `GAMES_ALL`, `GAMES_ELITE`
- `PPG_ALL`, `PPG_ELITE`, `PPG_DROP`, `PCT_DROP`
- `TS_PCT_ALL`, `TS_PCT_ELITE`

Find the biggest `PPG_DROP` and the smallest. **Write those numbers down** — you need them in the next step.

> If you want a prettier view, right-click `comparison.csv` → **Open With…** → **Excel** (if installed). Or in VS Code, install the free "Rainbow CSV" extension.

---

## Step 8 — Fill in the README answer

In the left sidebar, open `projects/01-volume-vs-elite-defenses/README.md`.

Find line 5:
```
**Answer:** (to fill in once you finish the analysis)
```

Replace it with something concrete, e.g.:
```
**Answer:** Star scorers (20+ PPG) drop from an average of XX.X PPG overall to YY.Y PPG against the top-5 defenses — about a Z% decline. [Biggest faller] loses the most (A.A PPG); [most consistent] barely budges (B.B PPG).
```

Fill in the numbers from `comparison.csv`. Keep it to 2-3 sentences max.

Save the file: **Ctrl + S**.

---

## Step 9 — Fill in the write-up

Open `projects/01-volume-vs-elite-defenses/writeup.md`. It's a template with blanks marked `___`. Fill them in using the numbers from `comparison.csv` and what the chart shows.

Aim for around 200 words total. Save with **Ctrl + S**.

---

## Step 10 — Commit and push everything to GitHub

In the terminal (make sure `(.venv)` is still showing), go back to the repo root:

```
cd ..\..
```

You should now be back at `...\NBA-Analytics-Portfolio>`.

**Stage every new/changed file:**

```
git add .
```

**Commit with a message:**

```
git commit -m "Project 01: opponent-adjusted scoring analysis"
```

**Push to GitHub:**

```
git push
```

**First time pushing:** A browser window or popup may ask you to log in to GitHub. Sign in with your account. If it asks about Git Credential Manager, click **Authorize**.

When `git push` finishes (returns to the prompt), refresh your GitHub repo page in the browser. You should see the new `01-volume-vs-elite-defenses` files: `src/`, `data/`, `figures/`, `writeup.md`, `requirements.txt`. Click into `README.md` and you'll see the headline chart rendered at the top — that's the publication-quality output.

---

## Step 11 — Make sure the chart shows on GitHub

On your GitHub repo page, navigate to:
`projects/01-volume-vs-elite-defenses/README.md`

The `![Headline chart](figures/headline.png)` line should now show the actual chart inline, not a broken-image icon. If it's broken, the most common reason is the `figures/` folder didn't get pushed. Run `git status` in the terminal — if it shows untracked files, redo Step 10.

---

## You're done with Project 01.

What you can show a recruiter:
- A public GitHub repo with a real analysis
- A clean methodology (game logs + opponent DRtg + tier buckets)
- One publication-quality figure
- A 200-word write-up
- Reproducible: `pip install -r requirements.txt` then `python src/analysis.py`

Next move: start Project 02 in a new folder (`projects/02-...`). Same structure (`src/`, `data/`, `figures/`, `README.md`, `writeup.md`).

---

## Troubleshooting

### "Running scripts is disabled on this system" when activating venv
Run this once, type `Y` when prompted, then re-do Step 3:
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### `(.venv)` never appears
You probably skipped `cd` back to the repo root. Type `cd C:\Users\User\Documents\Claude\Projects\ANALYTICS PORTFOLIO\NBA-Analytics-Portfolio` then try Step 3 again.

### `ModuleNotFoundError: No module named 'nba_api'`
The venv isn't active, OR the packages were installed outside it. Confirm `(.venv)` is on your prompt, then re-run:
```
pip install -r projects\01-volume-vs-elite-defenses\requirements.txt
```

### The script hangs on "Fetching player game logs"
NBA's API is rate-limited and sometimes slow. Wait 2 minutes. If still stuck, press `Ctrl + C` to cancel, wait 30 seconds, and re-run `python src/analysis.py`.

### `git push` says "Authentication failed"
You need a Personal Access Token, not your password. Quick path: install **GitHub CLI** from https://cli.github.com — then run `gh auth login` once and follow the browser prompts. After that, `git push` will work.

### Chart shows but names look wrong / empty / fewer than expected
Lower the thresholds at the top of `src/analysis.py`:
```
MIN_PPG_OVERALL = 18.0
MIN_GAMES_VS_ELITE = 8
```
Save, re-run `python src/analysis.py`.

### Want to use a different season
Change `SEASON = "2024-25"` near the top of `src/analysis.py` to e.g. `"2023-24"`. Save and re-run.
