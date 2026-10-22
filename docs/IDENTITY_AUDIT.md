# VelaBeat identity migration audit

Branch: feature/velabeat-identity. Do not merge into main or deploy production.

## Completed
- Unique mobile and TV application IDs, including dev flavors.
- Launcher display names.
- VelaBeat-specific UPDATE_APK_PREFIX values for mobile and TV.

## Not yet verified / migration gates
- Updater repository URL and update-check logic must be audited; changing APK prefix alone does not prevent contacting upstream releases. Disable upstream update checks until VelaBeat-owned release endpoint exists.
- Existing Android App Links refer to bitchord.kushagrasingh.in. Do not claim verification for VelaBeat; remove or replace only after a VelaBeat-controlled assetlinks.json is deployed.
- Custom bitchord://party scheme and Listen Together default server: changing these without tracing callers and QR generation may break invites; do not silently switch.
- Wear OS command and stream paths, watch package, bundled Wear APK and pairing: verify end-to-end before migration.
- Gradle verifyDevInstall task still checks com.dev.bitchord; update before using task.
- Provider authorities using ${applicationId} are appropriately scoped; retain Kotlin namespaces and fully-qualified classes for now.
- OAuth login, deep links, Cast, app widgets, file provider, Android Auto, MediaSession and background playback require device QA.

## CI gate
Build both mobile dev debug and TV debug variants on this branch. Record run ID, success conclusion, and artifact APK names. Resource reference checks alone are insufficient.
