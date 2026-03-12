# Quantum Vault

Quantum Vault is a mobile-first neon arcade maze game.

## Core Loop
- Collect every key shard in the district
- Decide whether to detour for optional high-value vault cores
- Chase fast-expiring bonus caches before they disappear
- Ride boost lanes for tempo, score flow, and cleaner escapes
- Charge and trigger Pulse Burst to stun nearby enemies
- Reach the exit before lockdown pressure drains the run

## What changed in this polish pass
- Added **score surge pickups** that temporarily juice every score event, give the HUD a clearer arcade multiplier readout, and create stronger route temptation mid-run
- Added a late-level **Vault Jackpot** that appears when the exit comes online, creating a real greed-vs-escape decision instead of every finish feeling the same
- Added glowing **boost lanes** that make certain routes faster and more aggressive, especially in Solar Breach
- Turned district themes into real gameplay modifiers instead of just color swaps:
  - **Prism Lock:** faster gate cadence
  - **Ion Bloom:** longer core-based gate jams and a little more clock generosity
  - **Velvet Circuit:** stronger combo/flow economy
  - **Solar Breach:** harsher timer pressure but hotter speed lanes and more volatile routing
- Improved the **arcade score feel** with a surge multiplier, stronger top-banner score callouts, better local leaderboard treatment, board placement at run end, and better best-score signaling
- Expanded **level-clear rewards** so exits now bank time, integrity, chain, core sweep, and cache sweep bonuses
- Improved motion and readability with more animated high-value pickups, stronger jackpot/surge moments, and more obvious state messaging when the room changes
- Improved **mobile-first control feel** by allowing drag steering during touch movement instead of waiting only for touch release
- Kept the game fully local and mobile-first, including swipe / drag / D-pad movement and a dedicated **Pulse Burst** action button

## Controls
- **Desktop:** WASD / Arrow keys to move, Space for Pulse Burst
- **Mobile:** swipe or use the D-pad, tap the Burst button for Pulse Burst

## Notes
- The game is fully self-contained and does not depend on external hosted assets.
- Scores and leaderboard entries are stored in local browser storage.
- Best results now come from balancing clean shard clears with smart cache greed instead of just pathing straight to the exit.
