"""Execute ads via Google Ads API."""
from __future__ import annotations


def launch_keyword(keyword: str, max_cpc: float, budget: float, campaign: str):
    try:
        from google.ads.googleads.client import GoogleAdsClient
    except Exception:  # pragma: no cover - optional
        raise RuntimeError("google-ads not installed")
    client = GoogleAdsClient.load_from_dict({})
    # Placeholder request
    return {
        "keyword": keyword,
        "cpc": max_cpc,
        "budget": budget,
        "campaign": campaign,
    }
