# Scripts — oai.studio Growth Automation

## Available Scripts

### 1. `seo_audit.py` — Full Site SEO Audit

Scans all oai.studio pages and checks title length, meta description, ALT tags, H1 tags, and internal links.

```bash
pip install requests beautifulsoup4
python3 seo_audit.py
```

**Output:** `seo_audit_YYYYMMDD.json` + `seo_audit_YYYYMMDD.csv`

---

### 2. `social_cover_generator.py` — Social Media Cover Generator

Converts product images to platform-optimized social media covers with brand overlay.

```bash
pip install Pillow
# Generate for all platforms:
python3 social_cover_generator.py --input product.jpg --platform all
# Generate for specific platform:
python3 social_cover_generator.py --input product.jpg --platform twitter
```

**Supported platforms:** twitter, reddit, pinterest, instagram, tiktok

**Output sizes:**
- Twitter/X: 1200×675px
- Reddit: 1200×900px  
- Pinterest: 1000×1500px
- Instagram: 1080×1080px
- TikTok: 1080×1920px

---

### 3. `alt_tag_audit.py` — Image ALT Tag Audit

Scans all product pages for missing or poor ALT tags and generates optimized suggestions.

```bash
pip install requests beautifulsoup4
python3 alt_tag_audit.py
```

**Output:** `alt_tag_audit_YYYYMMDD.csv` with current ALT and suggested optimized ALT

---

## Installation

```bash
pip install requests beautifulsoup4 Pillow
```

## Weekly Usage

Run every Monday before the weekly growth meeting:

```bash
python3 seo_audit.py
python3 alt_tag_audit.py
```

Review the CSV outputs and update Shopify admin accordingly.
