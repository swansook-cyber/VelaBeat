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

## Source-level findings (2026-10-23)
- `tv/src/main/java/com/music/bitchord/TvActivity.kt` is a dedicated `ComponentActivity` with `TvApp`, `BitChordTvTheme`, shared `MainViewModel`, `rememberMediaController` and `rememberPlayerState`. It attaches `TvRefreshRateController`, consumes playback/invite links, and pauses playback when finishing. These semantics need deliberate preservation.
- TV's manifest uses an exported `.MainActivity` **activity-alias** targeting non-exported `.TvActivity`; launcher includes both `LAUNCHER` and `LEANBACK_LAUNCHER` and `APP_MUSIC`. A single merged manifest cannot simply duplicate `.MainActivity` as both an activity and alias.
- Mobile's `MainActivity` is an `AppCompatActivity` with touch-focused Compose UI and activity-result handling; avoid replacing it globally.
- The TV module shares phone sources but its `TvActivity` and TV Compose UI are not automatically compiled into the phone `app` module. An app-module dependency/source-set strategy is needed before referencing TV classes.
- Proposed initial prototype: preserve mobile `MainActivity`; add an independently named TV entry activity to the app module, register only TV leanback launcher on it, and keep touch features optional. Confirm `TvApp` dependencies/resources compile before wiring runtime routing.
- Validate media session entry points: existing TV code aliases `.MainActivity` to `.TvActivity` for notifications/widgets, so a universal build needs explicit device-aware launch intents rather than assuming one activity name works on all devices.

## Build-path finding and safe fixes
- TV source overrides are selected by `replacedByTv` in `tv/build.gradle.kts`, which excludes phone Kotlin files sharing a relative path with TV replacements. Blindly adding the whole TV source directory to `app` would cause duplicate declarations or silently change phone behavior.
- Both `verifyDevInstall` Gradle tasks previously targeted `com.dev.bitchord`; fixed to the corresponding VelaBeat mobile/TV dev application IDs on this experimental branch.
- Compose TV dependencies include `androidx.tv:tv-material:1.0.0` and `androidx.tv:tv-foundation:1.0.0-alpha12`. They must be added to the chosen universal module only when the TV UI source inclusion strategy is ready.
- Next code gate: inventory every TV override and its references; decide between extracting a shared TV UI library module or selective inclusion into `app`. Prefer a shared library module to avoid duplicating classes.
- The universal build remains unimplemented; no CI result or device test is implied by these changes.
