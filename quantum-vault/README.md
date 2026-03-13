# Quantum Vault

Quantum Vault is a mobile-first neon maze arcade game built around one clean objective loop.

## Core loop
- Collect every shard in the room
- The portal opens when the room is clear
- Escape to move to the next zone
- Use Pulse Burst as your one simple panic button

## Current direction
This pass leans even harder into a fast, readable phone arcade loop:
- only one sentry early on, with the second enemy held back for later zones
- 4 to 6 shards per room so each layout reads quickly on a phone
- bigger shard pickup radius, faster Burst charging, and 4 lives for a more forgiving flow
- simpler scoring: shard points, escape bonus, zone clear, and clean escape reward
- improved local score chase with Best Zone tracking plus cleaner zone-first top-run labels
- richer animated backgrounds, brighter portal presentation, larger mobile play space, and smoother visual motion

## Controls
- **Desktop:** WASD / Arrow keys to move, Space for Pulse Burst
- **Mobile:** swipe / drag or use the D-pad, tap Burst to stun nearby sentries when charged

## Notes
- Fully self-contained; no external assets required
- Scores and leaderboard are stored in local browser storage
- Best runs come from quick collection routes, clean exits, and keeping mistakes low
