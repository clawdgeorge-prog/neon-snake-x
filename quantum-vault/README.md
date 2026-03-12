# Quantum Vault

Quantum Vault is a mobile-first neon arcade maze game.

## Core Loop
- Collect every key shard in the district
- Decide whether to detour for optional high-value vault cores
- Charge and trigger Pulse Burst to stun nearby enemies
- Reach the exit before lockdown pressure drains the run

## What changed in this polish pass
- Added a more arcade-style scoring model with chain growth, near-miss rewards, district clear bonuses, integrity bonuses, and speed bonuses
- Added optional **vault cores** to create better route decisions instead of a single obvious path every level
- Added a **local leaderboard** and much stronger best-score presentation
- Added a visible **district timer / lockdown pressure** for pacing and urgency
- Added a fourth enemy type (**hunter**) with telegraphed surge behavior
- Improved motion, particles, score popups, overlays, district themes, and HUD readability
- Improved mobile controls with a dedicated **Pulse Burst** action button

## Controls
- **Desktop:** WASD / Arrow keys to move, Space for Pulse Burst
- **Mobile:** swipe or use the D-pad, tap the Burst button for Pulse Burst

## Notes
- The game is fully self-contained and does not depend on external hosted assets.
- Scores and leaderboard entries are stored in local browser storage.
