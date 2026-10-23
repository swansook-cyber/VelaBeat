# VelaBeat single-APK feasibility audit

## Goal
One installable APK with one application ID for Android phone, tablet, Android TV and Android TV boxes. Touch and D-pad navigation should be selected according to device capabilities without replacing playback code.

## Verified from repository
- `app` and `tv` are distinct Gradle application modules, with separate application IDs and manifests.
- `tv/build.gradle.kts` already reuses `../app/src/main/java`, resources, assets, JNI libraries and CMake build; TV adds Compose TV UI and patches.
- TV manifest declares `android.software.leanback`, `android.hardware.touchscreen`, `LEANBACK_LAUNCHER`, `TvActivity`, and a TV banner.
- Mobile manifest includes multiple `LAUNCHER` entries; launcher and alias conflicts must be inspected before merging.
- Each module builds ABI-specific and multi-ABI universal APKs. Multi-ABI universal is **not** a single UI for all devices.
- Both modules depend on `:shared` and `:sharedUi`.

## Safe implementation plan (not yet implemented)
1. Inventory TV-specific classes/resources and overrides, especially `MainActivity`, `TvActivity`, Compose navigation and remote-focus handling.
2. Select one Gradle application module and one package ID. Prefer retaining `app` as base, without deleting `tv`.
3. Add TV activity, banner and LEANBACK_LAUNCHER in a merged manifest, with optional leanback and touchscreen features so neither TV nor touch-only devices are filtered out.
4. Detect UI mode at runtime; retain D-pad/OK/Back focus behavior and phone touch layouts.
5. Confirm file provider authorities, widgets, Android Auto, Wear, media session, playback, Cast and updater are preserved.
6. Build a separate experimental debug variant and verify manifest merged output, ABI APK sizes and clean installs on phone and TV.
7. Device QA: launcher visibility, remote focus, search keyboard, playback/background audio, deep links, updates, screen rotation and resume.
8. Keep existing mobile and TV artifacts until a universal build passes acceptance tests.

## Guardrails
- Do not copy the TV manifest over the mobile manifest wholesale.
- Do not merge source trees by text replacement: TV overrides can shadow app classes.
- Do not remove either existing module, merge into main, deploy or publish to Vela App Store without approval.
- This audit is not evidence that a single APK has built or passed QA.
