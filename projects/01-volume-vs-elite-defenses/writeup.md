# Volume vs. Elite Defenses — Write-up

*Fill the blanks below after `analysis.py` runs. Aim for ~200 words total.*

## Headline finding (2-3 sentences)
The average star scorer (20+ PPG) drops from **___ PPG against all opponents** to
**___ PPG against the league's top-5 defenses** — roughly a **___ percent** decline.
[Name the biggest faller and the most consistent star.]

## Why this matters for a GM (3-4 sentences)
Playoff opponents are uniformly closer to "elite" than the regular-season median.
A player whose volume collapses against good defenses is, in effect, padding stats
against weak schedules. [Name a contract or trade situation this lens informs.]

## What the chart shows (2-3 sentences)
The slope chart connects each player's all-opponent PPG (left) to their PPG vs.
top-5 DRtg defenses (right). Red lines flag drops of 3+ PPG; blue lines show
scorers whose production holds up.

## Caveats (1-2 sentences)
Season-average DRtg ignores in-game variance (injuries, rest, lineup shifts), and
the 10-game minimum vs. elite defenses still leaves some samples thin. The model
also does not adjust for home/away or back-to-backs.

## Method (1 sentence)
All player game logs for the season pulled via `nba_api`, joined to team season
DRtg, bucketed into Elite (1-5) / Good (6-15) / Average (16-20) / Poor (21-30),
then aggregated per player per tier.
