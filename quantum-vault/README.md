# Quantum Vault

Quantum Vault is a simpler, more mobile-first neon arcade maze game.

## Core loop
- Collect every shard in the maze
- The exit opens when the maze is clear
- Escape to advance to the next district
- Use Pulse Burst as a simple defensive panic button when charged

## What changed in this pass
- Simplified the run into **one obvious objective**: clear all shards, then reach the exit
- Tuned the game harder toward phones:
  - cleaner mobile layout
  - chunkier cards and controls
  - more forgiving lane-following turns so swipe input feels less fussy
- Simplified scoring into a clearer arcade model:
  - shard pickups are always worth straightforward points
  - each district has a visible **speed bonus** that drains over time
  - surviving with more lives adds a simple end-of-level bonus
  - local top scores still track your best runs
- Kept Pulse Burst as the one easy-to-read special move instead of layering in more systems
- Reduced drone scaling a bit so early runs stay readable and fair on a phone
- Improved presentation with richer drifting light beams, smoother motion, stronger glow, and a cleaner composition on small screens
- Kept the game instantly replayable after each loss

## Controls
- **Desktop:** WASD / Arrow keys to move, Space for Pulse Burst
- **Mobile:** swipe / drag or use the D-pad, tap Burst to stun nearby drones when charged

## Notes
- Fully self-contained; no external assets required
- Scores and leaderboard are stored in local browser storage
- Best results come from clearing efficiently, staying alive, and keeping the speed bonus alive
