#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from PIL import Image


# Palette ASCII du plus "clair" au plus "dense"
DEFAULT_RAMP = " .,:;i1tfLCG08@"
# Alternative plus contrastée (souvent mieux)
ALT_RAMP = " .:-=+*#%@"

def clamp(n: float, lo: float, hi: float) -> float:
    return lo if n < lo else hi if n > hi else n

def rgb_to_luma(r: int, g: int, b: int) -> float:
    # Luma perceptuelle (sRGB)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def ansi_fg(r: int, g: int, b: int) -> str:
    return f"\x1b[38;2;{r};{g};{b}m"

RESET = "\x1b[0m"

def image_to_ascii(
    img: Image.Image,
    width: int,
    ramp: str,
    color: bool,
    brightness: float,
    contrast: float,
    gamma: float,
    aspect: float,
) -> str:
    # Convertit en RGB
    img = img.convert("RGB")

    # Correction du ratio : les caractères sont plus hauts que larges.
    # aspect ~ 0.5 à 0.6 marche souvent bien selon la police/terminal.
    orig_w, orig_h = img.size
    height = max(1, int((orig_h / orig_w) * width * aspect))

    # Redimensionnement (LANCZOS = bonne qualité)
    img = img.resize((width, height), Image.LANCZOS)

    # Pré-calcul
    ramp_len = len(ramp)
    inv_255 = 1.0 / 255.0

    lines = []
    for y in range(height):
        line_parts = []
        for x in range(width):
            r, g, b = img.getpixel((x, y))

            # Luminance
            lum = rgb_to_luma(r, g, b) * inv_255  # 0..1

            # Ajustements (optionnels mais utiles pour "récupérer le fond")
            # contrast: >1 augmente le contraste, brightness: >1 éclaircit
            # gamma: <1 éclaircit les ombres, >1 assombrit
            lum = ((lum - 0.5) * contrast) + 0.5
            lum = lum * brightness
            lum = clamp(lum, 0.0, 1.0)
            lum = clamp(lum ** gamma, 0.0, 1.0)

            # Index dans la rampe (0 clair -> espace, fin dense -> @)
            idx = int(lum * (ramp_len - 1))
            ch = ramp[idx]

            if color:
                line_parts.append(ansi_fg(r, g, b) + ch)
            else:
                line_parts.append(ch)

        if color:
            line_parts.append(RESET)
        lines.append("".join(line_parts))

    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description="Convert an image to colored ASCII (ANSI TrueColor).")
    parser.add_argument("image", help="Path to image (png/jpg/...)")
    parser.add_argument("-w", "--width", type=int, default=0, help="Output width in characters (default: terminal width)")
    parser.add_argument("--ramp", default="alt", choices=["default", "alt"], help="ASCII ramp preset")
    parser.add_argument("--custom-ramp", default="", help="Custom ramp string from light->dense (overrides --ramp)")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI color (grayscale ASCII)")
    parser.add_argument("--brightness", type=float, default=1.05, help="Brightness multiplier (try 1.1-1.4)")
    parser.add_argument("--contrast", type=float, default=1.25, help="Contrast multiplier (try 1.2-2.0)")
    parser.add_argument("--gamma", type=float, default=0.85, help="Gamma (try 0.7-1.1). <1 reveals dark background")
    parser.add_argument("--aspect", type=float, default=0.55, help="Char aspect correction (0.45-0.65 typical)")
    args = parser.parse_args()

    term_w = shutil.get_terminal_size(fallback=(100, 30)).columns
    width = args.width if args.width > 0 else term_w

    ramp = DEFAULT_RAMP if args.ramp == "default" else ALT_RAMP
    if args.custom_ramp:
        ramp = args.custom_ramp

    img = Image.open(args.image)

    out = image_to_ascii(
        img=img,
        width=width,
        ramp=ramp,
        color=not args.no_color,
        brightness=args.brightness,
        contrast=args.contrast,
        gamma=args.gamma,
        aspect=args.aspect,
    )

    print(out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

