"""
Comprehensive test suite for the island counter assignment.
Tests all major functionality including core algorithm, file I/O, CLI interface,
error handling, and performance.
"""

from island_counter.main import count_and_map_islands, parse_file, main
import pytest
import tempfile
import os
import subprocess
import sys
import time
from unittest.mock import patch, mock_open
from io import StringIO

# Adjust the system path to include the project's root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Now, import from the correct package


class TestCoreAlgorithm:
    """Test the core island counting algorithm."""

    def test_empty_grid(self):
        """Test with empty grid."""
        assert count_and_map_islands([]) == 0

    def test_single_water_cell(self):
        """Test with single water cell."""
        grid = [['0']]
        assert count_and_map_islands(grid) == 0

    def test_single_land_cell(self):
        """Test with single land cell."""
        grid = [['1']]
        assert count_and_map_islands(grid) == 1

    def test_no_islands(self):
        """Test grid with only water."""
        grid = [
            ['0', '0', '0'],
            ['0', '0', '0'],
            ['0', '0', '0']
        ]
        assert count_and_map_islands(grid) == 0

    def test_all_land(self):
        """Test grid with all connected land."""
        grid = [
            ['1', '1', '1'],
            ['1', '1', '1'],
            ['1', '1', '1']
        ]
        assert count_and_map_islands(grid) == 1

    def test_diagonal_islands(self):
        """Test islands connected only diagonally (should be separate)."""
        grid = [
            ['1', '0', '0'],
            ['0', '1', '0'],
            ['0', '0', '1']
        ]
        assert count_and_map_islands(grid) == 3

    def test_u_shape_island(self):
        """Test U-shaped connected island."""
        grid = [
            ['1', '1', '1'],
            ['1', '0', '1'],
            ['1', '1', '1']
        ]
        assert count_and_map_islands(grid) == 1

    def test_multiple_islands(self):
        """Test multiple separate islands."""
        grid = [
            ['1', '1', '0', '0', '0'],
            ['1', '0', '0', '1', '1'],
            ['0', '0', '0', '1', '0'],
            ['0', '1', '0', '0', '0'],
            ['1', '1', '0', '0', '0']
        ]
        result = count_and_map_islands(grid)
        assert result == 3

    def test_complex_pattern(self):
        """Test with complex island pattern."""
        grid = [
            ['1', '0', '1', '0', '1'],
            ['0', '1', '0', '1', '0'],
            ['1', '0', '1', '0', '1'],
            ['0', '1', '0', '1', '0'],
            ['1', '0', '1', '0', '1']
        ]
        result = count_and_map_islands(grid)
        assert result == 13

    def test_large_connected_island(self):
        """Test with one large connected island."""
        grid = [
            ['1', '1', '1', '1', '1'],
            ['1', '0', '0', '0', '1'],
            ['1', '0', '1', '0', '1'],
            ['1', '0', '0', '0', '1'],
            ['1', '1', '1', '1', '1']
        ]
        result = count_and_map_islands(grid)
        assert result == 2


class TestFileProcessing:
    """Test file parsing and I/O operations."""

    def test_parse_valid_file(self):
        content = "010\n111\n010"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_path = f.name
        try:
            grid = parse_file(temp_path)
            expected = [['0', '1', '0'], ['1', '1', '1'], ['0', '1', '0']]
            assert grid == expected
        finally:
            os.unlink(temp_path)

    def test_parse_empty_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("")
            temp_path = f.name
        try:
            grid = parse_file(temp_path)
            assert grid == []
        finally:
            os.unlink(temp_path)

    def test_file_not_found(self):
        with pytest.raises(SystemExit):
            parse_file("nonexistent_file.txt")

    def test_invalid_characters(self):
        content = "010\n1X1\n010"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_path = f.name
        try:
            with pytest.raises(SystemExit):
                parse_file(temp_path)
        finally:
            os.unlink(temp_path)

    def test_non_rectangular_grid(self):
        content = "010\n11\n010"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_path = f.name
        try:
            with pytest.raises(SystemExit):
                parse_file(temp_path)
        finally:
            os.unlink(temp_path)


class TestCLIInterface:
    """Test command-line interface functionality."""

    def create_test_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.txt')
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_basic_execution(self):
        content = "010\n111\n010"
        temp_path = self.create_test_file(content)
        try:
            result = subprocess.run([
                sys.executable, '-m', 'island_counter.main', temp_path
            ], capture_output=True, text=True, timeout=10)
            assert result.returncode == 0
            assert "1" in result.stdout
        finally:
            os.unlink(temp_path)

    def test_visualization_flag(self):
        content = "010\n111\n010"
        temp_path = self.create_test_file(content)
        try:
            result = subprocess.run([
                sys.executable, '-m', 'island_counter.main', temp_path, '--visualize'
            ], capture_output=True, text=True, timeout=10)
            assert result.returncode == 0
            assert "1" in result.stdout
        finally:
            os.unlink(temp_path)

    def test_no_arguments(self):
        result = subprocess.run([
            sys.executable, '-m', 'island_counter.main'
        ], capture_output=True, text=True, timeout=10)
        assert result.returncode == 1
        assert "usage:" in result.stderr.lower() or "help" in result.stderr.lower()

    def test_invalid_file_path(self):
        result = subprocess.run([
            sys.executable, '-m', 'island_counter.main', 'nonexistent_file.txt'
        ], capture_output=True, text=True, timeout=10)
        assert result.returncode == 1
        assert "not found" in result.stderr.lower()


class TestPerformance:
    """Test performance with various grid sizes."""

    def generate_grid(self, rows, cols, land_probability=0.3):
        import random
        random.seed(42)
        grid = []
        for _ in range(rows):
            row = ['1' if random.random(
            ) < land_probability else '0' for _ in range(cols)]
            grid.append(row)
        return grid

    def test_small_grid_performance(self):
        grid = self.generate_grid(10, 10)
        start_time = time.time()
        result = count_and_map_islands([row[:] for row in grid])
        end_time = time.time()
        assert isinstance(result, int) and result >= 0
        assert (end_time - start_time) < 1.0

    def test_medium_grid_performance(self):
        grid = self.generate_grid(100, 100)
        start_time = time.time()
        result = count_and_map_islands([row[:] for row in grid])
        end_time = time.time()
        assert isinstance(result, int) and result >= 0
        assert (end_time - start_time) < 5.0

    def test_large_grid_performance(self):
        grid = self.generate_grid(500, 500)
        start_time = time.time()
        result = count_and_map_islands([row[:] for row in grid])
        end_time = time.time()
        assert isinstance(result, int) and result >= 0
        assert (end_time - start_time) < 30.0


class TestEdgeCases:
    """Test various edge cases and boundary conditions."""

    def test_single_row_grid(self):
        grid = [['1', '0', '1', '1', '0', '1']]
        assert count_and_map_islands(grid) == 3

    def test_single_column_grid(self):
        grid = [['1'], ['0'], ['1'], ['1'], ['0'], ['1']]
        assert count_and_map_islands(grid) == 3

    def test_alternating_pattern(self):
        grid = [
            ['1', '0', '1'],
            ['0', '1', '0'],
            ['1', '0', '1']
        ]
        assert count_and_map_islands(grid) == 5

    def test_border_islands(self):
        grid = [
            ['1', '1', '0', '0', '1'],
            ['0', '0', '0', '0', '1'],
            ['0', '0', '1', '0', '0'],
            ['0', '0', '0', '0', '0'],
            ['1', '0', '0', '0', '1']
        ]
        assert count_and_map_islands(grid) == 5


class TestDataIntegrity:
    """Test that the algorithm preserves data integrity."""

    def test_original_grid_unchanged_with_copy(self):
        original_grid = [['1', '0', '1'], ['1', '1', '0'], ['0', '1', '1']]
        grid_copy = [row[:] for row in original_grid]
        count_and_map_islands(grid_copy)
        assert original_grid == [['1', '0', '1'],
                                 ['1', '1', '0'], ['0', '1', '1']]

    def test_grid_modification_correct(self):
        grid = [['1', '0', '1'], ['1', '0', '0'], ['0', '0', '1']]
        result = count_and_map_islands(grid)
        assert result == 3
        island_ids = {cell for row in grid for cell in row if cell != '0'}
        assert len(island_ids) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
