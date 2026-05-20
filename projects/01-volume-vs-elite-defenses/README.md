# Project 1 — Volume vs. Elite Defenses

**Question:** How much does a star scorer's PPG drop against the league's top 5 defenses?

**Answer:** (to fill in once you finish the analysis)

![Headline chart](figures/headline.png)

## Method
- Pull all game logs via nba_api
- Join each game to opponent season DRtg
- Bucket opponents: elite (top 5), good (6–15), average (16–20), poor (21–30)
- Compute PPG and TS% per tier per player
- Filter to players with ≥10 games vs elite defenses

## Caveats
- Small samples vs elite opponents inflate variance
- Opponent DRtg is a season average — does not reflect injuries to the opposing defense

## Reproduce
\`\`\`bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
\`\`\`
