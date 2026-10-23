package com.music.bitchord.ui.car

import android.content.Context
import android.content.res.Configuration

/**
 * Presentation-only detection for a large landscape touchscreen, such as
 * an aftermarket Android head unit. Does not infer Android Auto support and
 * must never alter audio playback, media sessions, or driving permissions.
 *
 * Android TV remains on its own UI path. The minimum usable width is measured
 * in dp, not physical pixels, to avoid enabling car-style layouts on phones.
 */
object CarDisplayLayout {
    fun isEligible(
        context: Context,
        isTelevision: Boolean,
        minimumWidthDp: Int = 720
    ): Boolean {
        if (isTelevision) return false
        val configuration = context.resources.configuration
        val isLandscape = configuration.orientation == Configuration.ORIENTATION_LANDSCAPE
        val usableWidth = configuration.screenWidthDp
        val hasTouch = context.packageManager.hasSystemFeature(
            android.content.pm.PackageManager.FEATURE_TOUCHSCREEN
        )
        return isLandscape && hasTouch && usableWidth >= minimumWidthDp
    }
}
