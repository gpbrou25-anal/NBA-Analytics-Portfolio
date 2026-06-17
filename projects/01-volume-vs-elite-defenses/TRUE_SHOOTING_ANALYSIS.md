# True Shooting % — What the Scatter Chart's Color Dimension Actually Says

This is a supplementary analysis for [Project 1 — Volume vs. Elite Defenses](README.md), focused entirely on the color dimension of the scatter chart. The x-axis (PPG) and y-axis (win rate) tell one story. The color (True Shooting %) tells a different — and in some ways more important — one.

---

## What True Shooting % actually measures

Most basketball fans know field goal percentage. True Shooting % (TS%) is what you use when you want a real answer.

The formula is:

```
TS% = Points / (2 × (FGA + 0.44 × FTA))
```

Two adjustments make it more honest than FG%:

**It values the three-pointer correctly.** A made three gives you 50% more points than a made two. Plain FG% treats them identically — one make is one make. TS% weights by points actually scored, so a player who shoots 40% from three (1.2 points per attempt) is valued the same as a player shooting 60% from two (1.2 points per attempt). Plain FG% would call the first player a below-average shooter and the second an elite one. TS% calls them equal. It's right; FG% is wrong.

**It counts free throws as partial shot attempts.** The 0.44 multiplier on FTA is the key. It doesn't count every free throw as a full shot attempt — because most free throws come in pairs, and a two-shot trip to the line costs you one possession, not two. The 0.44 approximates the fraction of free throw attempts that represent full possession usage. It's been validated against play-by-play data for years; it's accurate enough that virtually every serious analyst uses it.

The result: TS% tells you how many points you produced per shot opportunity, counting threes at full value and the free throw line at its real cost. A TS% of 0.580 means you scored 58% of the theoretical maximum for your shot attempts. League average is consistently around 0.570–0.580. Stars should be above 0.600. Elite efficiency starts around 0.620. Below 0.530 against elite defenses is a real problem.

---

## Reading the scatter chart

The color in the scatter chart is each player's TS% in games specifically against Top-5 Defensive Rating teams. Not their season TS% — their TS% under maximum defensive pressure.

The scale runs from roughly 0.500 (dark purple, the bottom of the legend) to 0.675 (bright yellow-green, the top). Every player you see in the bottom-left of the color scale is shooting efficiently enough to make a good defense hurt. Every player in the dark purple is giving a good defense exactly what it wants.

Here is what the color dimension reveals that PPG alone cannot show.

---

## The three efficiency tiers visible in the data

### Tier 1: The efficient scorers (bright green to yellow, TS% ≥ 0.610)

**Victor Wembanyama — TS% ≈ 0.650**

The brightest color on the chart belongs to a 22-year-old in his third season. Wemby's position in the top-left corner (high win rate, moderate PPG) already tells you his team wins these games. The color tells you *why*: he produces points efficiently, without wasting possessions. He's not volume-scoring against elite defenses — he's scoring 22–23 points per game on shots that actually go in.

His shot diet against elite defenses is worth explaining. He gets most of his points from floaters, face-up mid-range, and post-ups — shot types that are inherently higher-percentage because they're close to the basket or taken against smaller defenders. He doesn't bomb away from three when the defense dares him. That discipline, at 22, is the thing scouts talk about that never shows up in a box score.

Social media currently debates whether Wemby is "really an elite scorer" because his PPG doesn't match SGA or Ant. The scatter chart's color dimension answers that: he is not a volume scorer, but he is an *efficient* one. Those are two different things. A GM building a team for the playoffs wants efficiency. Regular-season PPG rankings are secondary.

**Anthony Edwards — TS% ≈ 0.645**

The top-right section of the chart — scoring *and* winning against elite defenses — has very few players. Edwards is one of them, and his color confirms that his scoring against top defenses is real production, not just volume.

What makes his TS% hold up: Edwards attacks the basket, gets to the line at a high rate, and has developed a three-point shot that defenses can't ignore. Against elite defenses that try to funnel him left or take away the drive, he now has the pull-up jumper to punish them either way. That combination — rim pressure plus viable jumper — is what efficient scoring against elite defenses looks like. His TS% in elite-defense games being above 0.640 is the same profile, in different numbers, as what he showed in Minnesota's playoff runs.

The media narrative around Edwards in 2025–26 is "next face of the league." The TS% chart is a supporting argument they mostly haven't made yet: it's not just that he scores, it's that he scores *well* against the teams that matter.

---

### Tier 2: The solid performers (teal range, TS% ≈ 0.555–0.605)

**Shai Gilgeous-Alexander — TS% ≈ 0.580**

At first glance, SGA's color doesn't pop. He's in the middle of the scale — a clear yellow-green but not at the top. That seems odd for the best scorer in the dataset.

The explanation is specific to his game. SGA's scoring against elite defenses is built heavily on free throws. He shoots around 9–10 per game; against elite defenses that stay disciplined in help-side positioning, some of those attempts come from step-back contact rather than clean drives. His FTA rate stays high, but his two-point field goal percentage against elite defenses dips slightly as the help rotates faster. The result is a TS% that's above average but not at the top of the chart.

What matters is that his TS% holds *stable*. This is the key distinction between SGA and the players in Tier 3 below: his efficiency doesn't crater against elite defenses the way theirs does. He's not as color-bright as Edwards or Wemby, but he doesn't turn dark the way Mitchell does.

The broader point about SGA: his 31-point average against elite defenses (essentially flat from his overall season number) combined with a stable TS% means that his scoring production is real in every context. Volume doesn't come with a hidden efficiency cost when he faces a good defense. That is genuinely rare.

**Nikola Jokić — TS% ≈ 0.595**

Jokić's TS% in elite-defense games lands squarely in the "solid" range, but context makes it impressive. He operates almost entirely in the paint and at the elbow — shots that should theoretically get harder as defensive quality improves, because elite defenses can afford to send a second body at him on every drive.

The reason his TS% doesn't collapse: he controls the pace of the possession entirely. He won't take a bad shot because the play clock is running. He passes the ball away from pressure and resets. His usage rate against elite defenses probably drops (he creates more for teammates when the defense commits to him), which means his actual shot attempts are higher quality than they'd be for a player who forces the issue.

Jokić's TS% on this chart is a read-between-the-lines argument for a point analysts often make but rarely quantify: efficient post scoring is harder to take away than efficient perimeter scoring, because the efficiency comes from shot selection rather than athleticism. Defenses can't age out Jokić's TS% the way they can a driver who loses a step.

**Jamal Murray — TS% ≈ 0.600**

Murray's color lands near the top of the teal range. His TS% reflects what his role actually is: a shot-creator working off Jokić's gravity, not a primary ball-handler who has to generate his own look every possession. When Jokić draws the defense, Murray gets cleaner looks. Against elite defenses that can't fully commit to stopping both, he still finds them.

His 2023 Finals run — where he shot 55.7% from three in the clinching game — is the extreme version of this. Elite defenses don't fully neutralize him because they can't guard him and Jokić simultaneously. His TS% on this chart is the regular-season evidence for that structural advantage.

**Jaylen Brown — TS% ≈ 0.565**

Brown sits slightly below Murray in the teal range, which fits his profile. He scores against elite defenses through downhill drives and mid-range pull-ups — efficient but not perfectly so. The slight dip from the top of the teal range comes from his tendency to take pull-up jumpers off the dribble under pressure, a shot type that is inherently lower percentage than rim attacks or open threes.

What keeps his TS% in the "solid" tier: he doesn't hunt bad shots. His shot profile with Boston — built around transition opportunities, cuts, and pull-ups — doesn't depend on creating from the dribble in the half-court against a set defense. Against elite teams that take away the transition game, his half-court efficiency drops slightly but not to a problematic level.

**Cade Cunningham, Kawhi Leonard, Kevin Durant, Devin Booker, Tyrese Maxey, Deni Avdija, Jalen Brunson** — All land in the teal range, TS% approximately 0.555–0.590. Each for different reasons:

- **Cunningham**: efficient mid-range game; young enough that elite defenses still make unforced errors against him.
- **Kawhi**: career-long elite TS% comes from shot selection — never forces anything, always takes the same three shots. Even against elite defenses those shots are still efficient.
- **Durant**: the mid-range shot that no defense in NBA history has ever consistently taken away. His TS% stays solid even as his PPG dips slightly because the shot quality stays constant.
- **Booker**: efficient in Phoenix's system; slight TS% dip against elite defenses reflects the loss of easy picks when the defense hedges well.
- **Maxey**: high volume with a TS% that stays honest; his three-point shooting carries the efficiency.
- **Avdija**: the most interesting player in this tier from a TS% standpoint — his PPG actually goes *up* against elite defenses (+1.9 vs. overall), and his TS% stays in the solid range. That's unusual. It means he's both scoring more and scoring efficiently. Most players who score more in a spot do so by taking more shots, which dilutes TS%. Avdija doesn't.
- **Brunson**: ISO-heavy scorer whose TS% holds up because he doesn't need pace or space — just a pick and a clear path to the mid-post.

---

### Tier 3: The efficiency problem (dark range, TS% ≤ 0.530)

**Donovan Mitchell — TS% ≈ 0.502**

The darkest color on the chart, at a PPG level that should produce better efficiency. Mitchell scores around 22–23 points per game against elite defenses — the second-lowest PPG in the dataset among the big-dot players — and does it on enough attempts that his TS% hits roughly 0.500–0.505. That's below the league average for all players combined, including bench players, including role players who rarely touch the ball.

To score 22 points with a 0.500 TS%, you're burning through possessions. If you assume roughly 18–20 true shot attempts to score 22 points at 0.500 TS%, that's close to what you'd expect from a player working against maximum resistance — contested pull-ups, tough angles, no transition baskets. The volume drop and the efficiency drop arrive at the same time, which is a textbook description of a scorer who can't manufacture quality looks against elite opposition.

The social media narrative around Mitchell is "can't win in the playoffs." That framing is incomplete, but the TS% chart makes it concrete: it's not that he disappears — it's that the points he does score cost the Cavaliers too many possessions. An 0.500 TS% against top defenses means roughly 1-in-10 possessions used on his scoring produces zero expected value above league average. In a playoff series, that compounds.

**Luka Dončić — TS% ≈ 0.515**

Luka is the most interesting player in Tier 3 because his PPG in elite-defense games (~29–30) is close to his season overall, but his color is still dark. He's the largest-dot, darkest-color combination on the chart — which is exactly the definition of high-volume, low-efficiency scoring.

Why does his TS% drop against elite defenses even when his PPG doesn't drop much? The shot profile shifts. Against average and poor defenses, Luka gets easy looks off his step-back three and his pick-and-roll. Against elite defenses, the help rotates to the three-point line faster, the big who is supposed to roll to the basket hedges instead of trailing, and the step-back three becomes contested instead of semi-open. He still makes a reasonable percentage of them — Luka is a real shooter — but "reasonable" at that level of difficulty is 35–37%, down from the 40%+ he shoots against weaker teams.

The free throw rate doesn't fully compensate. His TS% against elite defenses reflects an offense that is running correctly (Luka running the pick-and-roll, getting to his spots) but producing slightly worse outcomes at the margin. The 0.515 isn't catastrophic. It explains, in one number, why his team's win rate against elite defenses is roughly 30%.

The media discussion around Luka's playoff limitations usually focuses on defense, conditioning, or leadership. The scatter chart adds an often-ignored piece: even his offense, the thing he was built to do, runs at notably lower efficiency against top defenses. A 0.515 TS% with 29–30 PPG volume means he's using possessions at a rate that good defenses are willing to live with.

---

## Why the current NBA media landscape mostly ignores TS% in real time — and why it matters

TS% doesn't trend on social media after games. Box scores do.

When Mitchell drops 34 points on a Wednesday night, the highlights are the deep pull-up threes, the mid-range over the close-out, the and-one. The fact that he went 12-for-28 from the field and used 24 possessions to get there doesn't make the graphic. The box score says 34 points. The conversation starts there and mostly ends there.

TS% entered mainstream NBA discourse around 2012–2015 as advanced stats went from niche to standard on sports media. But it's still mostly deployed as a *career* or *season-long* descriptor ("he's a 62% true shooter") rather than a game-context metric. Very few broadcasts or articles split a player's TS% by opponent defensive quality. That split is what this chart is doing — and it's where the real information lives.

Three specific narratives where this analysis rewrites the conventional take:

**"SGA is the best scorer in the league"** — The conventional case is his PPG and his MVP voting. The TS% chart adds a layer: his 0.580 against elite defenses isn't flashy, but it's steady. Most high-volume scorers see their TS% drop 3–6 points against elite defenses. SGA's barely moves. The *stability* of his efficiency, not just its level, is the argument.

**"Mitchell is a max-contract scorer"** — The conventional case is his PPG average and his Cleveland playoff appearances. The TS% chart complicates it: he's a 0.500 TS% scorer against the exact defenses a max contract is supposed to deliver results against. Max contracts are justified by performance in the hardest games. The hardest games are exactly where the TS% goes dark.

**"Luka's offense makes up for everything"** — The conventional case is that even his bad playoff runs include huge scoring nights. The TS% chart suggests that volume alone doesn't rescue the problem: 29–30 PPG at 0.515 TS% means the offense is running through him at a possession cost that elite defenses are winning. High points in a loss can still be low-efficiency scoring. Often is.

---

## The actual insight the color dimension adds

Separating the chart into PPG (x-axis, dot size), win rate (y-axis), and TS% (color) creates three independent variables that tell a complete story only when read together.

Here is the typology:

| PPG vs elite D | TS% vs elite D | Win rate | Player type | Examples |
|---|---|---|---|---|
| High | High | High | Playoff-ready scorer | Edwards |
| High | High | Low | Star on a weak team | SGA (early OKC) |
| High | Low | Low | Empty-calorie volume | Luka, Mitchell |
| Low | High | High | Efficient, system-supported | Wemby, Murray |
| Low | Low | Low | Benchable in big games | Lower-left players |

The category "high volume, low TS%, low win rate" is the one that generates the most misleading box scores and the most misaligned contracts in the NBA. Those players look great on a Tuesday in November and disappear in May. The color dimension of this chart is a real-time signal for which players belong in which category.

The most actionable read for roster construction: pay for the top-left of the chart (high TS%, winning games, moderate PPG) before you pay for the bottom-right (high PPG, low TS%, losing games). Wemby over Mitchell, at any price, for a playoff run. The box score says Mitchell is the bigger star. The TS% chart says you're wrong.

---

## A note on what TS% does not tell you here

TS% isn't pace-adjusted. Elite defenses tend to slow the game down — fewer possessions per game means fewer shot attempts per player, which can improve shot selection and artificially inflate TS% for some players. A scorer who takes 20 shots in a fast game and 15 in a slow one might post higher TS% in the slow game simply because the 15 shots were a cleaner subset. This analysis doesn't correct for pace.

TS% also doesn't capture *when* the shots happen. A player who makes five threes in garbage time and bricks six mid-range attempts in crunch time can post a perfectly average TS% that hides the crunch-time collapse. This chart uses season-level aggregates — it's the right scale for overall player valuation, not for fourth-quarter clutch analysis. That is a different project.

Finally, TS% reflects shot *quality* as much as shot *skill*. A player in a system that generates open looks will post higher TS% than an equal talent in a more isolation-heavy offense. This matters most for the teal-range players on this chart — some of them are efficient partly because their teammates create space, not purely because they're elite shotmakers. The Jokić effect on Murray is the clearest example in this dataset.

---

## Summary

True Shooting % in elite-defense games is one of the cleanest single-number tests of whether a scorer's production is real or inflated. The scatter chart's color dimension runs that test on 40 of the NBA's highest-volume scorers in 2025–26.

The findings:

- **Wembanyama and Edwards** lead the dataset in TS% against elite defenses. Both score above 0.640. Both win games in those spots. These are the profiles you build franchises around.
- **SGA's TS% stability** — not his level, but its stability against elite defenses — is the part of his case for best scorer in the league that social media hasn't fully articulated yet.
- **Mitchell and Luka** both fall below 0.530 TS% against elite defenses. Mitchell is worse. Both are high-volume, below-average-efficiency scorers in the games where the margin for error is smallest.
- **Jokić, Durant, Kawhi** are in the solid middle tier — their TS% holds up because their shot selection doesn't change with the defense. These are the scorers who age well in the playoffs.
- **Avdija** is the anomaly: he scores *more* against elite defenses *and* maintains a solid TS%. Whether that's a real effect or a sample artifact, it's the most contract-relevant finding in the dataset for a player on his next deal.

The box score will keep showing Mitchell's 34-point nights. The TS% chart is the honest second opinion.

---

*Methodology: TS% calculated for each player using points, FGA, and FTA from games only against Top-5 DRtg teams in 2025–26. Formula: PTS ÷ (2 × (FGA + 0.44 × FTA)). Source: NBA.com Stats API via nba_api.*
