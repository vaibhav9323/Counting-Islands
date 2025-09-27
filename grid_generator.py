import random


def generate_and_save_grid(height, width, filename="random_generated_input.txt"):
    """
    Generates a rectangular grid of a given height and width and saves it to a file.

    Args:
        height (int): The number of rows in the grid.
        width (int): The number of columns in the grid.
        filename (str): The name of the file to save the grid to.
    """
    if height <= 0 or width <= 0:
        print("Error: Please enter positive numbers for height and width.")
        return

    try:
        with open(filename, 'w') as f:
            for _ in range(height):
                # Create a list of random 0s and 1s for the row
                row = [str(random.randint(0, 1)) for _ in range(width)]
                # Write the row to the file, followed by a newline character
                f.write("".join(row) + '\n')

        print(
            f"\n✅ Successfully generated and saved a {height}x{width} grid to '{filename}'")

    except IOError as e:
        print(f"\n❌ Error: Could not write to file '{filename}'. Reason: {e}")


if __name__ == "__main__":
    try:
        # Prompt the user for the grid dimensions
        grid_height = int(
            input("Enter the height for the grid (number of rows): "))
        grid_width = int(
            input("Enter the width for the grid (number of columns): "))
        generate_and_save_grid(grid_height, grid_width)
    except ValueError:
        print("Invalid input. Please enter valid integers for the dimensions.")
