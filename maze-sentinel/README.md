# Maze Sentinel

Neon browser arcade prototype focused on maze-chase + route-control gameplay.

## Direction
- Not Pac-Man themed
- Strong neon / premium arcade visuals
- Mobile-friendly touch controls with drag steering and forgiving lane turn assist
- Built as the real target for the hourly OpenAI polishing cron

## Files
- `index.html` — playable prototype

## Current systems
- Four drone classes: Scout, Hunter, Glimmer, and Wraith
- Path-based pursuit so enemies can pressure routes more intelligently
- Hunter drones telegraph a lock-on reticle, then burst into short high-speed surges
- Wraith drones can phase through walls briefly, becoming intangible and faster while passing through obstacles — adding unpredictable movement patterns that force players to adapt routes on the fly
- Decoy beacon ability: place a temporary lure on your tile to bend pursuit lines and open safer escape lanes
- Arc-lash combo: trigger a pulse while a decoy is active to fire a crackling trap lane that stuns drones caught along the link
- District breach loop: collect a shard quota to open an exit portal, then reach it alive to clear the district
- Exit breach climax: once the portal opens you get a short visible escape window before it shifts somewhere else, making the end of each level feel more like a deliberate sprint than a cleanup lap
- Compact in-run HUD now shows breach progress alongside score / drones / district state
- Route-assist breadcrumb line now guides you toward the live objective (next shard or open exit), improving readability on touch screens without adding clutter
- Mobile handling now truly supports live continuous drag steering on the arena, plus forgiving lane-follow turn assist so quick thumb corrections land more reliably in tight corridors instead of waiting for swipe release
- New danger-sense readability pass adds a live danger meter, edge-of-screen threat arrows, and a player danger halo so nearby pressure and hunter surge setups are easier to read on mobile
- Drone roles are now objective-aware instead of only speed-based: scouts cut ahead on your breadcrumb route, glimmers lean toward anchoring the shard / exit, and hunters keep direct lock pressure
- A live Intel HUD pill now calls out whether the nearest pressure is Pursuit, Intercept, Anchor, Decoy, or an active Hunter Lock so route decisions read faster mid-run
- New intent telegraphs make drone roles readable at a glance: scouts now project cyan intercept lanes toward your route, glimmers tether gold anchor lines into the live objective, and hunters keep their lock reticles / surge rails
- Accessibility pass adds one-tap reduced-motion and high-contrast toggles, persisted locally for repeat runs across mobile and desktop
- District theme rotation is now mechanical as well as visual:
  - **Astra / Flux Reserve** — pulse costs less charge
  - **Velour / Mirage Grid** — decoys last longer and recharge faster
  - **Sol / Overcharge Lattice** — pulse expands farther and stuns longer
  - **Nyx / Blink Mesh** — gates recycle faster after warps
- Level clears now get a short premium-feeling breach transition with a celebratory audio stinger, district confirmation card, and a cleaner handoff into the next themed sector instead of abruptly snapping into the next run state
- Adaptive soundtrack now changes by district and swells during hunter locks / exit-rush pressure so the run has more cinematic momentum even before new content is added
- New ability-readiness strip makes pulse charge, decoy restock progress, and arc-lash priming readable at a glance, while the Pulse / Decoy touch buttons now glow or dim based on live availability
- New in-canvas tactical radar gives a compact live overview of maze walls, player position, drones, gate anchors, decoys, shard / exit location, and your current breadcrumb route — especially useful on mobile when pressure gets dense
- New flow-scoring system rewards stylish clean play: risky shard pickups, multi-drone arc-lash stuns, and fast portal breaches now build a live multiplier, with floating callouts, light audio feedback, and a subtle screen glow that makes momentum readable without cluttering the maze
- New **Overdrive** system turns close calls into a reward loop: skim drones without taking a hit to gain a short speed surge, bonus charge, extra score, and a gold-lit visual state that makes high-risk route threading feel more intentional
- Polished **title screen** with animated pulsing logo, best score / districts cleared stats, keyboard controls reference, and accessibility toggles for reduced motion and high contrast (all persisted locally)
- Game over screen now displays score, districts cleared, and best score with option to return to title
- Audio layering pass adds distinct sound effects for drone spawns, overdrive activation, and upgrade purchases — giving better aural feedback for key gameplay moments
- Wall collision feedback: bumping into walls now triggers themed particle sparks, a subtle dual-tone audio bump, micro screen shake, and haptic vibration on supported devices — adding tactile responsiveness to movement
- Portal warp cinematics: when you reach the exit, your character spirals into the portal with a shrink animation, swirling vortex effects, and screen glow before the district transition
- District arrival celebration: enhanced particle bursts with new district colors, stronger camera shake, screen flash, and a celebratory callout announcing the new district when you breach
- Enhanced ability visual effects: pulse burst now has multi-ring expansion with shockwave and radiating particles, decoy beacon features rotating energy rays and pulsing energy field, arc-lash combo has electric crackling with branching sparks and traveling energy pulses plus screen flash on hit
- Additional particle burst upgrades on ability activation for more tactile feedback

## Next polish ideas
- more enemy variety
