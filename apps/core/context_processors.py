"""
Global template context processors for HJ Opportunity Hub.

These values are injected into every template's context automatically,
so things like site branding or global stats don't need to be passed
manually from every view. Expanded in Phase 6 with real site-wide data
(e.g., category list for nav, saved-count badge, etc.).
"""


def site_settings(request):
    """
    Provides site-wide constants available in all templates.
    Placeholder for Phase 2 — expanded significantly in Phase 6.
    """
    return {
        "SITE_NAME": "HJ Opportunity Hub",
        "SITE_TAGLINE": "Your Gateway to Opportunities in Liberia & Africa",
    }