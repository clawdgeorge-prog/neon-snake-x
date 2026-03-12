# Maze Sentinel

Neon browser arcade prototype focused on maze-chase + route-control gameplay.

## Direction
- Not Pac-Man themed
- Strong neon / premium arcade visuals
- Mobile-friendly touch controls
- Built as the real target for the hourly OpenAI polishing cron

## Files
- `index.html` — playable prototype

## Current systems
- Three drone classes: Scout, Hunter, and Glimmer
- Path-based pursuit so enemies can pressure routes more intelligently
- Hunter drones telegraph a lock-on reticle, then burst into short high-speed surges
- Decoy beacon ability: place a temporary lure on your tile to bend pursuit lines and open safer escape lanes
- Arc-lash combo: trigger a pulse while a decoy is active to fire a crackling trap lane that stuns drones caught along the link
- District breach loop: collect a shard quota to open an exit portal, then reach it alive to clear the district
- Compact in-run HUD now shows breach progress alongside score / drones / district state
- Route-assist breadcrumb line now guides you toward the live objective (next shard or open exit), improving readability on touch screens without adding clutter
- New danger-sense readability pass adds a live danger meter, edge-of-screen threat arrows, and a player danger halo so nearby pressure and hunter surge setups are easier to read on mobile
- District theme rotation is now mechanical as well as visual:
  - **Astra / Flux Reserve** — pulse costs less charge
  - **Velour / Mirage Grid** — decoys last longer and recharge faster
  - **Sol / Overcharge Lattice** — pulse expands farther and stuns longer
  - **Nyx / Blink Mesh** — gates recycle faster after warps

## Next polish ideas
- richer soundtrack / SFX system
- title screen, progression, unlocks
- smarter drone synergies and telegraphed threat moments
- stronger portal presentation / completion cinematics
- district-specific VFX/audio stingers when traits rotate in
