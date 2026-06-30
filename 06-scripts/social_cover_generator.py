#!/usr/bin/env python3
"""
oai.studio Social Media Cover Image Generator
Generates platform-specific cover images with brand overlay
Usage: python3 social_cover_generator.py --input product.jpg --platform twitter
"""

import argparse
from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Platform specifications
PLATFORMS = {
    "twitter": {"size": (1200, 675), "name": "Twitter/X"},
    "reddit": {"size": (1200, 900), "name": "Reddit"},
    "pinterest": {"size": (1000, 1500), "name": "Pinterest"},
    "instagram": {"size": (1080, 1080), "name": "Instagram"},
    "tiktok": {"size": (1080, 1920), "name": "TikTok Cover"},
}

# Brand colors
BRAND_PINK = (255, 182, 193)      # Light pink
BRAND_CREAM = (255, 248, 240)     # Cream white
BRAND_DARK = (80, 60, 55)         # Dark brown text
OVERLAY_COLOR = (255, 255, 255, 40)  # Semi-transparent white


def add_brand_overlay(img, platform_name):
    """Add oai.studio brand overlay to image."""
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size

    # Bottom gradient overlay
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Draw semi-transparent bottom bar
    bar_height = int(h * 0.12)
    overlay_draw.rectangle(
        [(0, h - bar_height), (w, h)],
        fill=(255, 255, 255, 180)
    )
    img = Image.alpha_composite(img.convert("RGBA"), overlay)

    # Add brand text
    draw = ImageDraw.Draw(img)

    # Try to use a system font, fall back to default
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(h * 0.035))
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(h * 0.025))
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Brand name
    brand_text = "oai.studio"
    url_text = "oai.studio/collections"

    # Position text at bottom
    text_y = h - bar_height + int(bar_height * 0.2)
    draw.text((int(w * 0.05), text_y), brand_text, fill=BRAND_DARK, font=font_large)
    draw.text((int(w * 0.05), text_y + int(h * 0.04)), url_text, fill=(120, 100, 95), font=font_small)

    # Tagline on right
    tagline = "Handmade in Kyoto"
    draw.text((int(w * 0.6), text_y + int(h * 0.01)), tagline, fill=BRAND_DARK, font=font_small)

    return img.convert("RGB")


def generate_cover(input_path, platform, output_dir="."):
    """Generate a social media cover for the specified platform."""
    if platform not in PLATFORMS:
        print(f"Unknown platform: {platform}. Choose from: {', '.join(PLATFORMS.keys())}")
        return None

    spec = PLATFORMS[platform]
    target_size = spec["size"]

    # Open and resize image
    try:
        img = Image.open(input_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

    # Convert to RGBA for overlay operations
    img = img.convert("RGBA")

    # Smart crop to target aspect ratio
    orig_w, orig_h = img.size
    target_w, target_h = target_size
    target_ratio = target_w / target_h
    orig_ratio = orig_w / orig_h

    if orig_ratio > target_ratio:
        # Image is wider than target — crop sides
        new_w = int(orig_h * target_ratio)
        left = (orig_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, orig_h))
    else:
        # Image is taller than target — crop top/bottom
        new_h = int(orig_w / target_ratio)
        top = (orig_h - new_h) // 4  # Slightly above center for product shots
        img = img.crop((0, top, orig_w, top + new_h))

    # Resize to target
    img = img.resize(target_size, Image.LANCZOS)

    # Add brand overlay
    img = add_brand_overlay(img, spec["name"])

    # Save output
    input_name = os.path.splitext(os.path.basename(input_path))[0]
    output_filename = f"{input_name}_{platform}.jpg"
    output_path = os.path.join(output_dir, output_filename)

    img.save(output_path, "JPEG", quality=92)
    print(f"Generated: {output_path} ({target_w}x{target_h}px)")
    return output_path


def batch_generate(input_path, output_dir="."):
    """Generate covers for all platforms."""
    print(f"Generating social covers for: {input_path}")
    print(f"Output directory: {output_dir}\n")

    os.makedirs(output_dir, exist_ok=True)
    generated = []

    for platform in PLATFORMS:
        result = generate_cover(input_path, platform, output_dir)
        if result:
            generated.append(result)

    print(f"\nGenerated {len(generated)} cover images.")
    return generated


def main():
    parser = argparse.ArgumentParser(
        description="oai.studio Social Media Cover Generator"
    )
    parser.add_argument("--input", required=True, help="Input product image path")
    parser.add_argument(
        "--platform",
        default="all",
        choices=list(PLATFORMS.keys()) + ["all"],
        help="Target platform (default: all)"
    )
    parser.add_argument("--output-dir", default="./social-covers", help="Output directory")

    args = parser.parse_args()

    if args.platform == "all":
        batch_generate(args.input, args.output_dir)
    else:
        os.makedirs(args.output_dir, exist_ok=True)
        generate_cover(args.input, args.platform, args.output_dir)


if __name__ == "__main__":
    main()
