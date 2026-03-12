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
- Added **real risky route decisions** with bonus credit caches that expire fast and pay best when you grab them early
- Added glowing **boost lanes** that make certain routes faster and more aggressive, especially in Solar Breach
- Turned district themes into real gameplay modifiers instead of just color swaps:
  - **Prism Lock:** faster gate cadence
  - **Ion Bloom:** longer core-based gate jams and a little more clock generosity
  - **Velvet Circuit:** stronger combo/flow economy
  - **Solar Breach:** harsher timer pressure but hotter speed lanes and more volatile routing
- Improved the **arcade score feel** with stash tracking, stronger banner presentation, better best-score emphasis, richer score popups, and a punchier run-end summary
- Expanded **level-clear rewards** so exits now bank time, integrity, chain, core sweep, and cache sweep bonuses
- Improved motion and readability with more lane signaling, more animated pickups, and clearer high-value moments inside the maze
- Kept the game fully local and mobile-first, including swipe / D-pad movement and a dedicated **Pulse Burst** action button

## Controls
- **Desktop:** WASD / Arrow keys to move, Space for Pulse Burst
- **Mobile:** swipe or use the D-pad, tap the Burst button for Pulse Burst

## Notes
- The game is fully self-contained and does not depend on external hosted assets.
- Scores and leaderboard entries are stored in local browser storage.
- Best results now come from balancing clean shard clears with smart cache greed instead of just pathing straight to the exit.
