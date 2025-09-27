import sys
import argparse
from collections import deque
from typing import List, Set, Tuple

# ANSI escape codes for colors
COLORS = [
    "\033[91m",  # Red
    "\033[92m",  # Green
    "\033[93m",  # Yellow
    "\033[94m",  # Blue
    "\033[95m",  # Magenta
    "\033[96m",  # Cyan
]
RESET_COLOR = "\033[0m"


def print_colored_grid(grid: List[List[str]]):
    """Prints the grid with colored islands for visualization."""
    print("\nVisual Map of Islands:")
    for row in grid:
        for cell in row:
            if cell.isdigit() and cell != '0':
                color_index = (int(cell) - 1) % len(COLORS)
                print(f"{COLORS[color_index]}{'#'}{RESET_COLOR}", end="")
            else:
                print("~", end="")
        print()


def count_and_map_islands(grid: List[List[str]]) -> int:
    """
    Counts the number of islands and maps them on the grid for visualization.
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    island_count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                island_count += 1
                island_id = str(island_count + 1)

                q = deque([(r, c)])
                grid[r][c] = island_id

                while q:
                    row, col = q.popleft()

                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nr, nc = row + dr, col + dc

                        if (0 <= nr < rows and
                            0 <= nc < cols and
                                grid[nr][nc] == '1'):

                            grid[nr][nc] = island_id
                            q.append((nr, nc))

    return island_count


def parse_file(file_path: str) -> List[List[str]]:
    """
    Parses the input file into a 2D list of characters.
    """
    try:
        with open(file_path, 'r') as f:
            grid = [list(line.strip()) for line in f if line.strip()]

        if grid:
            first_row_len = len(grid[0])
            if not all(len(row) == first_row_len for row in grid):
                raise ValueError("Input grid is not rectangular.")

            valid_chars = {'0', '1'}
            for r_idx, row in enumerate(grid):
                for c_idx, char in enumerate(row):
                    if char not in valid_chars:
                        raise ValueError(
                            f"Invalid character '{char}' at row {r_idx+1}, col {c_idx+1}.")

        return grid
    except FileNotFoundError:
        print(
            f"Error: The file at path '{file_path}' was not found.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Main function to parse command-line arguments and run the island counter.
    """
    parser = argparse.ArgumentParser(
        description="Counts the number of islands in a 2D map from a file.",
        epilog="The file should contain '0's for water and '1's for land."
    )
    parser.add_argument(
        "filepath",
        metavar="<path_to_the_file>",
        type=str,
        help="Path to the input file containing the island map."
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Display a visual map of the islands in the terminal."
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    grid = parse_file(args.filepath)

    grid_for_mapping = [row[:] for row in grid]
    result = count_and_map_islands(grid_for_mapping)

    print(result)

    if args.visualize:
        print_colored_grid(grid_for_mapping)


if __name__ == "__main__":
    main()
