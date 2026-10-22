# VelaBeat branding baseline

Project: VelaBeat (fork of BitChord). Preserve upstream license and attribution.

## Approved initial identity
- Name: VelaBeat
- Visual: neon V + music note + play triangle; dark navy background, magenta/violet/cyan gradient.
- Launcher: symbol-only, no wordmark; use separate full logo for splash and store artwork.
- Platforms: Android phone/tablet and Android TV.

## Implementation gate
1. Import generated PNG assets from the conversation deliverable into Android resources; verify asset provenance and dimensions.
2. Verify Android launcher adaptive icon foreground/background and monochrome icon. Do not just overwrite the legacy launcher bitmap.
3. Provide TV banner (landscape) separately; square launcher artwork is not a valid substitute.
4. Set app label and distinct application IDs for phone and TV, including dev variants, after baseline CI is green.
5. Audit app update URLs, provider identifiers, OAuth redirects, deep links, authorities and Wear pairing before package rename.
6. Test install side-by-side with original BitChord and existing Vela Music; confirm launcher, D-pad focus and lockscreen media controls.
7. Never merge to main or deploy to production without approval.

## CI
Baseline workflow: .github/workflows/velabeat-baseline.yml. Debug-only, no upstream signing secrets.

## Asset status
Artwork created outside GitHub; binary Android resources not committed yet. Do not mark icon integration complete until PNGs are imported, build succeeds, and device tests pass.
