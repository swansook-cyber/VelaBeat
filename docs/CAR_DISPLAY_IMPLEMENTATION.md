# VelaBeat Car Display — implementation gates

## Verified on user's Android head unit
- Android 15; display reported as 1280×720; 4 GB RAM.
- 32-bit ARM APK installed after arm64 APK failed.
- Home, recommendations, playlists, and queue rendered.
- User confirmed music audio output and next-track playback.
- Steering wheel buttons, lock-screen playback, and Android TV remote are not yet verified.

## Scope
One APK across supported Android form factors. Car Display is an adaptive
large-landscape-touch presentation mode, **not** Android Auto and not a
certified automotive app. Never assume all landscape tablets are cars.

## Implementation sequence
1. Detect landscape touch display, excluding TV; expose explicit user
   preference before enabling a new UI (auto/off/on).
2. Refactor the mini-player layout to keep playback controls visible and
   separated from the bottom navigation at 1280×720.
3. Add larger touch targets (48dp minimum; prefer 56dp for transport).
4. Preserve existing media player, queue, media session, account state,
   navigation and package ID.
5. Test on 32-bit ARM head unit first, then phone portrait, tablet
   landscape and Android TV with remote.

## Acceptance
- Existing phone and TV builds still pass.
- Experimental combined-source build passes.
- Head-unit playback, pause, next, previous, back and navigation work.
- Mini-player never obscures song rows or bottom navigation.
- UI mode can be disabled if the display is misclassified.
- No changes to Production, main, Vela Music, or Vela App Store.
