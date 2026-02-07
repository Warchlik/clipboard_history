# Clipboard History

A CLI tool for managing and tracking system clipboard history.

## Project Description

Clipboard History is a console application written in Python that enables:
- **Clipboard Monitoring** - automatically track everything you copy
- **History Management** - browse, search, and delete entries
- **Persistent Storage** - SQLite database for long-term access

## Installation

### Requirements
- Python 3.13+
- `uv` - package manager (https://github.com/astral-sh/uv)

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/Warchlik/clipboard_history
cd clipboard_history

# 2. Install the tool (in the main directory)
uv tool install -e .

# 3. If you want to uninstall a previous version
uv tool uninstall clipboard
```

## Usage

### Help
```bash
clip --help
```

### Available Commands

| Command | Description |
|---------|-------------|
| `clip list [value]` | Displays clipboard history, optionally filtered by value |
| `clip search [value]` | Searches through clipboard history |
| `clip watch` | Monitors clipboard in real-time |
| `clip prune` | Cleans and removes old entries |

### Usage Examples

```bash
# Display entire history
clip list

# Search through history
clip search "my keywords"

# Watch clipboard in real-time
clip watch

# Clean up older entries
clip prune
```

## Technology

- **Python** 3.13+
- **SQLAlchemy** (>=2.0.46) - ORM for database operations
- **Typer** (>=0.21.1) - CLI interface creation
- **pyperclip** (>=1.11.0) - system clipboard access
- **platformdirs** (>=4.5.1) - directory path management

## Project Structure

```
clipboard_history/
├── src/
│   └── cli.py           # Main CLI application file
├── pyproject.toml       # Project configuration
├── uv.lock              # Dependency lock file
└── README.md            # This file
```

## Notes for Developers

### Running in dev mode
```bash
uv run python -m src.cli clip --help
```
