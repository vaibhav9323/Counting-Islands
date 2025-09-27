# Island Counter

## 📝 Introduction

This project is a solution for a recruitment task that involves counting the number of islands in a 2D map provided as a text file. The map consists of '0's (water) and '1's (land). An island is defined as a group of '1's connected horizontally or vertically.

This solution is designed to be efficient, scalable, and easy to use. It includes a command-line interface, comprehensive unit tests, and Docker support for easy deployment.

---

## ✨ Features

* **Efficient Island Counting**: Uses a Breadth-First Search (BFS) algorithm to efficiently count islands without running into stack overflow issues.
* **Command-Line Interface**: A user-friendly CLI to run the program, with clear instructions and error handling.
* **Visualization**: An optional `--visualize` flag to display a colored map of the islands in the terminal.
* **Dockerized**: Comes with a `Dockerfile` for easy containerization and deployment.
* **Comprehensive Tests**: Includes a full suite of unit, integration, and performance tests.
* **Cross-Platform**: Includes shell scripts for both Linux/macOS (`.sh`) and Windows (`.bat`).

---

## 🚀 Getting Started

### Prerequisites

* **Docker**: The primary way to run this project is with Docker. Make sure you have Docker installed and running on your system.
* **Python 3.10+** (for local development): If you want to run the project locally without Docker, you'll need Python 3.10 or newer.

### Installation and Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd island-counter
    ```

2.  **Build the Docker image**:
    ```bash
    ./build.sh
    ```
    This will build a Docker image named `island-counter:latest`.

---

## Usage

To count the islands in a map file, use the `run.sh` script (or `run.bat` on Windows) followed by the path to your input file.

### Examples

* **Basic Usage**:
    ```bash
    ./run.sh small_islands.txt
    ```
    Output:
    ```
    3
    ```

* **With Visualization**:
    ```bash
    ./run.sh medium_islands.txt --visualize
    ```
    This will output the number of islands and also print a colored map to your terminal.

* **Help Message**:
    To see the full list of options, run the script without any arguments:
    ```bash
    ./run.sh
    ```

---

## 🧪 Testing

The project includes a comprehensive test suite to ensure everything is working correctly.

To run all tests, you can use the provided `run_tests.py` script:

```bash
python3 tests/run_tests.py
```
This will execute:
1. Unit Tests: Core algorithm logic.
2. Integration Tests: File I/O and CLI functionality.
3. Error Handling Tests: How the application handles bad input.
4. Performance Tests: How the application performs with large grids.
## 📁 Project Structure

```
.
├── island_counter/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── data/
│   │   ├── ... (test files)
│   ├── run_tests.py
│   ├── test_comprehensive.py
│   └── test_main.py
├── .gitignore
├── build.sh
├── Dockerfile
├── README.md
├── requirements.txt
├── run.bat
└── run.sh
```

---
## 📦 Dependencies

The only external dependency is `pytest` for running the tests. It's listed in the `requirements.txt` file.

---

## 💡 Further Development

- **Unified Testing with `pytest`**: The integration and error handling tests in `run_tests.py` could be moved into the `pytest` framework for a more unified testing approach.
    
- **Support for Different Input Formats**: The application could be extended to support other input formats like JSON or CSV.
    
- **Performance Optimization**: For extremely large grids, further optimizations like parallel processing could be explored.
    

---

## 👨‍💻 Author

**Vaibhav Singala**
