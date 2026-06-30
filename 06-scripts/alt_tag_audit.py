#!/usr/bin/env python3
"""
oai.studio Image ALT Tag Audit & Batch Optimizer
Scans all product images and generates optimized ALT tag suggestions
Usage: python3 alt_tag_audit.py
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime

BASE_URL = "https://oai.studio"

# Product pages to scan
PRODUCT_PAGES = [
    "/products/pudding-boat-the-cream-bear-oai-studio",
    "/products/oai-studio-toast-cream-bear-keycap",
    "/products/lemonade-the-little-cream-bear-oai-studio",
    "/products/grape-soda-the-little-cream-bear-oai-studio",
    "/products/ramune-the-cream-bear-oai-studio",
    "/products/chocolate-raspberry-the-cream-bear-oai-studio",
    "/products/apple-the-cream-bear-oai-studio",
    "/products/picnic-fruit-basket-the-cream-bear-oai-studio",
    "/products/crystal-ball-magic-cat-keycap-pink-purple-nebula-cat-transparent-glossy-mechanical-keyboard-keycap",
    "/products/ocean-magic-cat-series-artisan-keycaps-one-piece-hand-painted-maritime-set-oai-studio",
    "/products/chinese-food-panda-keycaps-oai-studio",
    "/products/gift-kitty-oai-studio",
    "/products/strawberry-cream-delight-series-artisan-keycap-set-oai-studio",
]

# ALT tag generation rules
ALT_RULES = {
    "cream_bear": "Cream Bear artisan keycap {variant} - handmade kawaii keycap Oai Studio",
    "magic_cat": "Magic Cat artisan keycap {variant} - crystal resin keycap Oai Studio",
    "panda": "Foodie Panda artisan keycap {variant} - kawaii keyboard accessory Oai Studio",
    "gift_kitty": "Gift Kitty artisan keycap {variant} - cute cat keycap Oai Studio",
    "default": "{product_name} artisan keycap - handmade kawaii keyboard companion Oai Studio",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OAIStudioAltBot/1.0)"
}


def generate_alt_suggestion(img_src, product_title, current_alt):
    """Generate an optimized ALT tag suggestion."""
    filename = img_src.split("/")[-1].split("?")[0].lower()

    # Determine product type
    if "cream_bear" in filename or "creamy_bear" in filename:
        template = ALT_RULES["cream_bear"]
    elif "magic_cat" in filename or "crystal" in filename:
        template = ALT_RULES["magic_cat"]
    elif "panda" in filename:
        template = ALT_RULES["panda"]
    elif "kitty" in filename or "cat" in filename:
        template = ALT_RULES["gift_kitty"]
    else:
        template = ALT_RULES["default"]

    # Extract variant from filename
    variant = ""
    color_keywords = ["strawberry", "lemonade", "grape", "ramune", "chocolate",
                      "toast", "apple", "pink", "blue", "green", "red", "white"]
    for color in color_keywords:
        if color in filename:
            variant = color.replace("_", " ").title()
            break

    suggested = template.format(
        variant=variant,
        product_name=product_title[:50] if product_title else "artisan keycap"
    ).strip()

    return suggested


def audit_page_images(url):
    """Audit images on a single page."""
    full_url = BASE_URL + url
    results = []

    try:
        resp = requests.get(full_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return results

        soup = BeautifulSoup(resp.text, "html.parser")
        product_title = ""
        title_tag = soup.find("h1")
        if title_tag:
            product_title = title_tag.text.strip()

        images = soup.find_all("img")
        for img in images:
            src = img.get("src", "")
            alt = img.get("alt", None)

            # Skip tiny icons and SVGs
            if not src or "svg" in src or "icon" in src.lower():
                continue

            # Only audit product/content images
            if "cdn/shop" not in src and "cdn.shopify" not in src:
                continue

            issue = None
            if alt is None:
                issue = "MISSING_ALT"
            elif alt.strip() == "":
                issue = "EMPTY_ALT"
            elif len(alt) < 10:
                issue = "ALT_TOO_SHORT"
            elif len(alt) > 125:
                issue = "ALT_TOO_LONG"

            suggested_alt = generate_alt_suggestion(src, product_title, alt)

            results.append({
                "page_url": full_url,
                "product_title": product_title,
                "img_src": src[:100],
                "current_alt": alt if alt is not None else "(missing)",
                "issue": issue or "OK",
                "suggested_alt": suggested_alt if issue else alt,
            })

    except Exception as e:
        print(f"Error auditing {url}: {e}")

    return results


def run_alt_audit():
    """Run full ALT tag audit."""
    print(f"Starting ALT tag audit at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    all_results = []

    for page in PRODUCT_PAGES:
        print(f"  Scanning: {page}")
        results = audit_page_images(page)
        all_results.extend(results)

    # Statistics
    total = len(all_results)
    issues = [r for r in all_results if r["issue"] != "OK"]
    missing = [r for r in all_results if r["issue"] == "MISSING_ALT"]
    empty = [r for r in all_results if r["issue"] == "EMPTY_ALT"]

    print(f"\n{'='*60}")
    print("ALT TAG AUDIT SUMMARY")
    print(f"{'='*60}")
    print(f"Total images scanned: {total}")
    print(f"Images with issues: {len(issues)} ({len(issues)/total*100:.1f}%)")
    print(f"  - Missing ALT: {len(missing)}")
    print(f"  - Empty ALT: {len(empty)}")
    print(f"  - Other issues: {len(issues) - len(missing) - len(empty)}")

    # Save CSV with suggestions
    filename = f"alt_tag_audit_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["page_url", "product_title", "img_src", "current_alt",
                      "issue", "suggested_alt"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nFull report saved: {filename}")
    print("Use 'suggested_alt' column to update ALT tags in Shopify admin.")

    return all_results


if __name__ == "__main__":
    run_alt_audit()
