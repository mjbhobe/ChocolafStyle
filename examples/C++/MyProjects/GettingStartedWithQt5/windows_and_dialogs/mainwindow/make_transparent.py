from collections import deque
from PIL import Image


def remove_outer_background(
    image_path: str, output_path: str, tolerance: int = 25
) -> None:
    """Removes outer contiguous white background using a BFS boundary flood-fill algorithm.

    Args:
        image_path: Path to the input image file.
        output_path: Path to save the transparent PNG.
        tolerance: Color distance tolerance (0-255) for off-white variations.
    """
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()

    # Get the reference background color from top-left corner (0,0)
    target_r, target_g, target_b, _ = pixels[0, 0]

    visited = set()
    queue = deque()

    # Seed the flood fill from all four outer image borders
    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))

    def is_similar(r: int, g: int, b: int) -> bool:
        return (
            abs(r - target_r) <= tolerance
            and abs(g - target_g) <= tolerance
            and abs(b - target_b) <= tolerance
        )

    # 4-directional neighborhood offsets
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Process contiguous background pixels
    while queue:
        x, y = queue.popleft()

        if (x, y) in visited:
            continue
        visited.add((x, y))

        r, g, b, a = pixels[x, y]

        if is_similar(r, g, b):
            # Set alpha channel to 0 (Fully Transparent)
            pixels[x, y] = (r, g, b, 0)

            # Add neighboring unvisited pixels to the processing queue
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    queue.append((nx, ny))

    img.save(output_path, "PNG")
    print(f"Success! Saved transparent image to: {output_path}")


if __name__ == "__main__":
    remove_outer_background("file_open.png", "file_open_transparent.png")
