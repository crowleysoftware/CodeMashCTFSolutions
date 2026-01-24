#!/usr/bin/env python3
"""
R/Place CTF Canvas Maintainer
Continuously monitors and maintains your image on the canvas.
"""

import math
import random
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict, Any
import time
import argparse
from PIL import Image


# Configuration
BASE_URL = "https://rplace.ctf.digital"
CANVAS_WIDTH = 320
CANVAS_HEIGHT = 180
MAX_PARALLEL_THREADS = 100  # Number of concurrent requests
LOOP_DELAY = 2  # Seconds to wait between loops

# Will be populated from the loaded image
TARGET_PIXELS = []
PIXEL_COLORS = {}  # Maps (x, y) -> color hex string


def load_and_scale_image(
    image_path: str,
    stretch: bool = False,
    transparency_color: Tuple[int, int, int] = None,
    scale_percent: float = 100.0,
    position_x: int = None,
    position_y: int = None
) -> Tuple[Image.Image, Tuple[int, int, int, int]]:
    """
    Load an image and scale it to fit the canvas.

    Args:
        image_path: Path to the image file (PNG or JPG)
        stretch: If True, stretch to fill canvas; if False, maintain aspect ratio
        transparency_color: RGB tuple for transparent pixels (default: None = black)
        scale_percent: Scale percentage where 100 = max size that fits (default: 100)
        position_x: X coordinate for top-left corner (default: None = centered)
        position_y: Y coordinate for top-left corner (default: None = centered)

    Returns:
        Tuple of (scaled PIL Image in RGB mode, bounds tuple (x, y, width, height))
    """
    img = Image.open(image_path)

    # Convert to RGB, handling transparency
    if img.mode == 'RGBA' or img.mode == 'LA' or (img.mode == 'P' and 'transparency' in img.info):
        # Create background with transparency color (or black if not specified)
        bg_color = transparency_color or (0, 0, 0)
        background = Image.new('RGB', img.size, bg_color)
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    if stretch:
        # Stretch to fill entire canvas
        img = img.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.Resampling.LANCZOS)
        return img, (0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)

    # Calculate scaling factor to fit within canvas while maintaining aspect ratio
    orig_width, orig_height = img.size
    scale_w = CANVAS_WIDTH / orig_width
    scale_h = CANVAS_HEIGHT / orig_height
    scale = min(scale_w, scale_h)

    # Apply the scale percentage (100% = fits canvas, 50% = half that size)
    scale = scale * (scale_percent / 100.0)

    # Calculate new dimensions
    new_width = max(1, int(orig_width * scale))
    new_height = max(1, int(orig_height * scale))

    # Scale the image
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Calculate offset - use provided position or center
    if position_x is not None:
        offset_x = position_x
    else:
        offset_x = (CANVAS_WIDTH - new_width) // 2

    if position_y is not None:
        offset_y = position_y
    else:
        offset_y = (CANVAS_HEIGHT - new_height) // 2

    return img, (offset_x, offset_y, new_width, new_height)


def extract_pixel_colors(
    img: Image.Image,
    bounds: Tuple[int, int, int, int]
) -> Dict[Tuple[int, int], str]:
    """
    Extract color for each pixel from the image within the given bounds.

    Args:
        img: PIL Image (scaled)
        bounds: Tuple of (offset_x, offset_y, width, height) for canvas placement

    Returns:
        Dictionary mapping canvas (x, y) coordinates to hex color strings
    """
    colors = {}
    offset_x, offset_y, width, height = bounds

    for img_x in range(width):
        for img_y in range(height):
            r, g, b = img.getpixel((img_x, img_y))
            hex_color = f"{r:02x}{g:02x}{b:02x}"
            # Map to canvas coordinates
            canvas_x = offset_x + img_x
            canvas_y = offset_y + img_y
            colors[(canvas_x, canvas_y)] = hex_color

    return colors


def get_canvas_state() -> Dict[str, Any]:
    """
    Get the current state of the canvas.
    
    Returns:
        Dictionary containing canvas data or error information
    """
    try:
        response = requests.get(f"{BASE_URL}/get", timeout=10)
        
        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json()
            }
        else:
            return {
                'success': False,
                'error': f"HTTP {response.status_code}"
            }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_pixel_color(canvas_data: Any, x: int, y: int) -> str:
    """
    Extract the color of a specific pixel from canvas data.
    Modify this based on the actual structure of the canvas data.
    
    Args:
        canvas_data: The canvas data from the API
        x: X coordinate
        y: Y coordinate
        
    Returns:
        Color string of the pixel, or None if not found
    """
    try:
        return canvas_data['canvas'][x][y]
    except (KeyError, IndexError, TypeError):
        return None


def set_pixel(x: int, y: int, color: str) -> Dict[str, Any]:
    """
    Set a pixel to a specific color.
    
    Args:
        x: X coordinate
        y: Y coordinate
        color: Color to set (hex format without #)
        
    Returns:
        Dictionary containing result information
    """
    try:
        # print(f"Setting {x}, {y}, to {color}")
        url = f"{BASE_URL}/change?x={x}&y={y}&col={color}"
        response = requests.get(url, timeout=10)
        
        return {
            'coords': (x, y),
            'status_code': response.status_code,
            'success': response.status_code == 200,
            'url': url
        }
    except requests.exceptions.RequestException as e:
        return {
            'coords': (x, y),
            'status_code': None,
            'success': False,
            'error': str(e)
        }


def parallel_set_pixels(
    pixels: List[Tuple[int, int]],
    pixel_colors: Dict[Tuple[int, int], str],
    max_threads: int = 10
) -> List[Dict[str, Any]]:
    """
    Set multiple pixels in parallel using per-pixel colors.

    Args:
        pixels: List of (x, y) coordinate tuples
        pixel_colors: Dictionary mapping (x, y) to hex color
        max_threads: Maximum number of concurrent threads

    Returns:
        List of result dictionaries
    """
    results = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_pixel = {
            executor.submit(set_pixel, x, y, pixel_colors[(x, y)]): (x, y)
            for x, y in pixels
        }

        for future in as_completed(future_to_pixel):
            coords = future_to_pixel[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({
                    'coords': coords,
                    'status_code': None,
                    'success': False,
                    'error': f"Exception: {str(e)}"
                })

    return results


def main():
    """
    Main loop to continuously maintain your image on the canvas.
    """
    global TARGET_PIXELS, PIXEL_COLORS

    parser = argparse.ArgumentParser(
        description="R/Place CTF Canvas Maintainer - Paint an image or solid color on the canvas"
    )
    parser.add_argument(
        "image",
        nargs="?",
        default=None,
        help="Path to image file (PNG or JPG) to paint on canvas"
    )
    parser.add_argument(
        "--color", "-c",
        type=str,
        help="Single hex color to fill canvas (e.g., 'ff0000' for red)"
    )
    parser.add_argument(
        "--stretch", "-s",
        action="store_true",
        help="Stretch image to fill canvas (ignores aspect ratio)"
    )
    parser.add_argument(
        "--background", "-b",
        type=str,
        default=None,
        help="Fill letterbox area with this color (e.g., '000000'); if omitted, letterbox pixels are ignored"
    )
    parser.add_argument(
        "--transparency", "-t",
        type=str,
        default=None,
        help="Color to use for transparent pixels (e.g., 'ffffff'); also sets background default if not specified"
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=100.0,
        help="Scale percentage where 100%% = max size that fits canvas (default: 100)"
    )
    parser.add_argument(
        "--x",
        type=int,
        default=None,
        help="X coordinate for top-left corner of image (default: centered)"
    )
    parser.add_argument(
        "--y",
        type=int,
        default=None,
        help="Y coordinate for top-left corner of image (default: centered)"
    )
    parser.add_argument(
        "--repeat-x",
        type=int,
        default=1,
        help="Number of copies in the X axis (default: 1)"
    )
    parser.add_argument(
        "--repeat-y",
        type=int,
        default=1,
        help="Number of copies in the Y axis (default: 1)"
    )
    parser.add_argument(
        "--tile",
        action="store_true",
        help="Fill canvas with copies from --x/--y position (defaults to 0,0; overrides --repeat-x, --repeat-y)"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=MAX_PARALLEL_THREADS,
        help=f"Number of parallel threads (default: {MAX_PARALLEL_THREADS})"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=LOOP_DELAY,
        help=f"Delay between iterations in seconds (default: {LOOP_DELAY})"
    )
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Randomize the x/y starting position on each loop iteration"
    )
    args = parser.parse_args()

    # Validate arguments
    if not args.image and not args.color:
        parser.error("Either an image file or --color must be provided")
    if args.image and args.color:
        parser.error("Cannot use both image file and --color at the same time")

    # Set up pixel colors based on input mode
    if args.color:
        # Single color mode - strip '#' if present
        color = args.color.lstrip('#').lower()
        if len(color) != 6:
            parser.error("Color must be a 6-character hex code (e.g., 'ff0000')")
        print(f"Using solid color: #{color}")
        PIXEL_COLORS = {
            (x, y): color
            for x in range(CANVAS_WIDTH)
            for y in range(CANVAS_HEIGHT)
        }
        source_desc = f"Solid color #{color}"
    else:
        # Image mode - parse transparency color if specified
        transparency_rgb = None
        if args.transparency:
            trans_hex = args.transparency.lstrip('#').lower()
            if len(trans_hex) != 6:
                parser.error("Transparency color must be a 6-character hex code (e.g., 'ffffff')")
            transparency_rgb = (int(trans_hex[0:2], 16), int(trans_hex[2:4], 16), int(trans_hex[4:6], 16))
            print(f"Using transparency color: #{trans_hex}")

        # Handle position: use specified values, or default to (0,0) for tile mode
        position_x = args.x
        position_y = args.y
        if args.tile:
            if position_x is None:
                position_x = 0
            if position_y is None:
                position_y = 0

        print(f"Loading image: {args.image}")
        try:
            img, bounds = load_and_scale_image(
                args.image,
                stretch=args.stretch,
                transparency_color=transparency_rgb,
                scale_percent=args.scale,
                position_x=position_x,
                position_y=position_y
            )
            if args.stretch:
                print(f"Image stretched to {CANVAS_WIDTH}x{CANVAS_HEIGHT}")
            else:
                offset_x, offset_y, width, height = bounds
                position_type = "positioned" if args.x is not None or args.y is not None else "centered"
                scale_info = f" at {args.scale}%" if args.scale != 100.0 else ""
                print(f"Image scaled to {width}x{height}{scale_info}, {position_type} at ({offset_x}, {offset_y})")
        except Exception as e:
            print(f"Failed to load image: {e}")
            return
        PIXEL_COLORS = extract_pixel_colors(img, bounds)

        # Calculate repeat counts
        offset_x, offset_y, width, height = bounds
        repeat_x = args.repeat_x
        repeat_y = args.repeat_y

        # Handle --tile flag: calculate copies needed to fill canvas from starting position
        if args.tile and width > 0 and height > 0:
            # Calculate how many copies needed to fill from offset to canvas edge
            repeat_x = math.ceil((CANVAS_WIDTH - offset_x) / width)
            repeat_y = math.ceil((CANVAS_HEIGHT - offset_y) / height)
            print(f"Tiling: {repeat_x}x{repeat_y} copies starting at ({offset_x}, {offset_y})")

        # Create repeated copies if requested
        if repeat_x > 1 or repeat_y > 1:
            original_colors = PIXEL_COLORS.copy()
            for copy_y in range(repeat_y):
                for copy_x in range(repeat_x):
                    if copy_x == 0 and copy_y == 0:
                        continue  # Skip the original
                    x_offset = copy_x * width
                    y_offset = copy_y * height
                    for (orig_x, orig_y), color in original_colors.items():
                        new_x = orig_x + x_offset
                        new_y = orig_y + y_offset
                        # Only include if within canvas bounds
                        if 0 <= new_x < CANVAS_WIDTH and 0 <= new_y < CANVAS_HEIGHT:
                            PIXEL_COLORS[(new_x, new_y)] = color
            if not args.tile:
                print(f"Created {repeat_x}x{repeat_y} grid of copies")

        # Add letterbox pixels if background color is explicitly specified
        if args.background is not None and not args.stretch:
            bg_hex = args.background.lstrip('#').lower()
            if len(bg_hex) != 6:
                parser.error("Background color must be a 6-character hex code (e.g., '000000')")
            print(f"Filling letterbox with #{bg_hex}")
            for x in range(CANVAS_WIDTH):
                for y in range(CANVAS_HEIGHT):
                    if (x, y) not in PIXEL_COLORS:
                        PIXEL_COLORS[(x, y)] = bg_hex

        source_desc = args.image

    TARGET_PIXELS = list(PIXEL_COLORS.keys())

    # Store base pixel colors for random mode (colors relative to 0,0 origin)
    BASE_PIXEL_COLORS = {}
    img_width = 0
    img_height = 0
    if args.random and not args.color:
        # Calculate base colors relative to image origin
        min_x = min(x for x, y in PIXEL_COLORS.keys())
        min_y = min(y for x, y in PIXEL_COLORS.keys())
        max_x = max(x for x, y in PIXEL_COLORS.keys())
        max_y = max(y for x, y in PIXEL_COLORS.keys())
        img_width = max_x - min_x + 1
        img_height = max_y - min_y + 1
        BASE_PIXEL_COLORS = {
            (x - min_x, y - min_y): color
            for (x, y), color in PIXEL_COLORS.items()
        }

    print(f"R/Place CTF Canvas Maintainer")
    print(f"Source: {source_desc}")
    print(f"Monitoring {len(TARGET_PIXELS)} pixels")
    print(f"Parallel threads: {args.threads}")
    print(f"Loop delay: {args.delay}s")
    if args.random:
        print(f"Random mode: enabled (randomizing position each iteration)")
    print("=" * 80)
    print("Press Ctrl+C to stop\n")

    iteration = 0

    try:
        while True:
            iteration += 1
            print(f"\n[Iteration {iteration}] {time.strftime('%H:%M:%S')}")

            # Randomize position if random mode is enabled
            if args.random and BASE_PIXEL_COLORS:
                # Calculate valid random position range
                max_start_x = CANVAS_WIDTH - img_width
                max_start_y = CANVAS_HEIGHT - img_height
                rand_x = random.randint(0, max(0, max_start_x))
                rand_y = random.randint(0, max(0, max_start_y))
                print(f"Random position: ({rand_x}, {rand_y})")

                # Recalculate pixel positions with new offset
                PIXEL_COLORS = {
                    (x + rand_x, y + rand_y): color
                    for (x, y), color in BASE_PIXEL_COLORS.items()
                    if 0 <= x + rand_x < CANVAS_WIDTH and 0 <= y + rand_y < CANVAS_HEIGHT
                }
                TARGET_PIXELS = list(PIXEL_COLORS.keys())

            # Get current canvas state
            print("Fetching canvas state...", end=" ")
            canvas_result = get_canvas_state()

            if not canvas_result['success']:
                print(f"Failed: {canvas_result.get('error', 'Unknown error')}")
                time.sleep(args.delay)
                continue

            print("Done")
            canvas_data = canvas_result['data']

            # Check which pixels need updating
            pixels_to_update = []
            for x, y in TARGET_PIXELS:
                current_color = get_pixel_color(canvas_data, x, y)
                target_color = PIXEL_COLORS[(x, y)]
                if current_color != "#" + target_color:
                    pixels_to_update.append((x, y))

            if not pixels_to_update:
                print(f"All {len(TARGET_PIXELS)} pixels are correct!")
            else:
                print(f"{len(pixels_to_update)}/{len(TARGET_PIXELS)} pixels need updating")
                print(f"Updating pixels...", end=" ")

                # Update pixels in parallel
                results = parallel_set_pixels(
                    pixels_to_update,
                    PIXEL_COLORS,
                    args.threads
                )

                # Count successes
                success_count = sum(1 for r in results if r['success'])
                print(f"{success_count}/{len(results)} updated")

                # Show failures if any
                failures = [r for r in results if not r['success']]
                if failures:
                    print("  Failures:")
                    for f in failures[:5]:  # Show first 5 failures
                        error_msg = f.get('error') or f"HTTP {f.get('status_code')}"
                        print(f"    {f['coords']}: {error_msg}")

            # Wait before next iteration
            print(f"Waiting {args.delay}s...", end="", flush=True)
            time.sleep(args.delay)
            print(" Done")

    except KeyboardInterrupt:
        print("\n\nStopped by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
