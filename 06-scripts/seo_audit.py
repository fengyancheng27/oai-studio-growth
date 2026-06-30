#!/usr/bin/env python3
"""
oai.studio SEO Audit Script
Scans all pages and checks: title length, meta description, ALT tags, internal links
Usage: python3 seo_audit.py
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
import time

BASE_URL = "https://oai.studio"

PAGES_TO_AUDIT = [
    "/",
    "/collections/artisan-keycaps",
    "/collections/frontpage",
    "/collections/special-keys",
    "/collections/little-panda-kitchen",
    "/collections/gift-kitty-family",
    "/collections/full-keycap-set",
    "/collections/mechanical-switches",
    "/products/pudding-boat-the-cream-bear-oai-studio",
    "/products/oai-studio-toast-cream-bear-keycap",
    "/products/lemonade-the-little-cream-bear-oai-studio",
    "/products/grape-soda-the-little-cream-bear-oai-studio",
    "/products/crystal-ball-magic-cat-keycap-pink-purple-nebula-cat-transparent-glossy-mechanical-keyboard-keycap",
    "/products/strawberry-cream-delight-series-artisan-keycap-set-oai-studio",
    "/blogs/studio-note",
    "/blogs/studio-note/why-i-wanted-softer-keycaps",
    "/blogs/studio-note/a-day-in-the-studio",
    "/blogs/studio-note/how-little-characters-become-companions",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OAIStudioSEOBot/1.0; +https://oai.studio)"
}


def audit_page(url):
    """Audit a single page for SEO issues."""
    full_url = BASE_URL + url
    result = {
        "url": full_url,
        "status_code": None,
        "title": None,
        "title_length": 0,
        "meta_description": None,
        "meta_desc_length": 0,
        "h1_count": 0,
        "h1_text": None,
        "images_total": 0,
        "images_missing_alt": 0,
        "images_empty_alt": 0,
        "internal_links": 0,
        "external_links": 0,
        "issues": [],
        "score": 0,
    }

    try:
        resp = requests.get(full_url, headers=HEADERS, timeout=15)
        result["status_code"] = resp.status_code

        if resp.status_code != 200:
            result["issues"].append(f"HTTP {resp.status_code}")
            return result

        soup = BeautifulSoup(resp.text, "html.parser")

        # Title
        title_tag = soup.find("title")
        if title_tag:
            result["title"] = title_tag.text.strip()
            result["title_length"] = len(result["title"])
            if result["title_length"] < 30:
                result["issues"].append(f"Title too short ({result['title_length']} chars)")
            elif result["title_length"] > 60:
                result["issues"].append(f"Title too long ({result['title_length']} chars)")
        else:
            result["issues"].append("Missing title tag")

        # Meta Description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            result["meta_description"] = meta_desc["content"]
            result["meta_desc_length"] = len(result["meta_description"])
            if result["meta_desc_length"] < 120:
                result["issues"].append(f"Meta description too short ({result['meta_desc_length']} chars)")
            elif result["meta_desc_length"] > 160:
                result["issues"].append(f"Meta description too long ({result['meta_desc_length']} chars)")
        else:
            result["issues"].append("Missing meta description")

        # H1 Tags
        h1_tags = soup.find_all("h1")
        result["h1_count"] = len(h1_tags)
        if h1_tags:
            result["h1_text"] = h1_tags[0].text.strip()[:100]
        if result["h1_count"] == 0:
            result["issues"].append("Missing H1 tag")
        elif result["h1_count"] > 1:
            result["issues"].append(f"Multiple H1 tags ({result['h1_count']})")

        # Images
        images = soup.find_all("img")
        result["images_total"] = len(images)
        for img in images:
            alt = img.get("alt")
            if alt is None:
                result["images_missing_alt"] += 1
            elif alt.strip() == "":
                result["images_empty_alt"] += 1

        if result["images_missing_alt"] > 0:
            result["issues"].append(f"{result['images_missing_alt']} images missing ALT")
        if result["images_empty_alt"] > 0:
            result["issues"].append(f"{result['images_empty_alt']} images with empty ALT")

        # Links
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"]
            if href.startswith("http") and BASE_URL not in href:
                result["external_links"] += 1
            elif href.startswith("/") or BASE_URL in href:
                result["internal_links"] += 1

        # Score calculation
        score = 100
        score -= len(result["issues"]) * 10
        score -= result["images_missing_alt"] * 3
        score -= result["images_empty_alt"] * 2
        result["score"] = max(0, score)

    except Exception as e:
        result["issues"].append(f"Error: {str(e)}")

    return result


def run_audit():
    """Run full site audit and save results."""
    print(f"Starting oai.studio SEO audit at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Auditing {len(PAGES_TO_AUDIT)} pages...\n")

    results = []
    for page in PAGES_TO_AUDIT:
        print(f"  Auditing: {page}")
        result = audit_page(page)
        results.append(result)
        time.sleep(1)  # Be polite to the server

    # Save JSON report
    report_filename = f"seo_audit_{datetime.now().strftime('%Y%m%d')}.json"
    with open(report_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Save CSV report
    csv_filename = f"seo_audit_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["url", "status_code", "score", "title", "title_length",
                      "meta_desc_length", "h1_count", "images_total",
                      "images_missing_alt", "images_empty_alt",
                      "internal_links", "external_links", "issues"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            row = {k: r.get(k, "") for k in fieldnames}
            row["issues"] = "; ".join(r.get("issues", []))
            writer.writerow(row)

    # Print summary
    print("\n" + "="*60)
    print("SEO AUDIT SUMMARY")
    print("="*60)
    avg_score = sum(r["score"] for r in results) / len(results)
    print(f"Average Score: {avg_score:.1f}/100")
    print(f"Pages with missing meta description: {sum(1 for r in results if 'Missing meta description' in r['issues'])}")
    print(f"Pages with missing H1: {sum(1 for r in results if 'Missing H1 tag' in r['issues'])}")
    total_missing_alt = sum(r['images_missing_alt'] for r in results)
    print(f"Total images missing ALT: {total_missing_alt}")
    print(f"\nReports saved: {report_filename}, {csv_filename}")

    return results


if __name__ == "__main__":
    run_audit()
