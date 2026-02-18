# Automated Python Docstring Generator

A powerful tool to **automatically generate docstrings**, analyze documentation coverage, enforce PEP-257 compliance, and apply fixes — built for Python developers and teams.

### Milestones Achieved

- **Milestone 1**: AST-based parsing → identify functions/classes, extract params/returns, generate baseline docstrings, coverage report
- **Milestone 2**: Multi-style generation (Google, NumPy, reST) + compliance checks (PEP-257 via pydocstyle)
- **Milestone 3**: Streamlit UI with interactive upload, preview, generation, and apply functionality
- **Milestone 4**: Pip-installable package, robust edge-case tests, UI polish (search, filters, tooltips), CLI entry point, full documentation

## Features

- Parses Python code with AST
- Generates docstrings in **Google**, **NumPy**, or **reST** style
- Coverage analysis (documented/missing percentage, missing sections)
- PEP-257 compliance checking
- Interactive **Streamlit UI** with search, missing-only filter, and auto-apply
- Batch CLI for folders/files
- Robust tests for edge cases (empty files, syntax errors, etc.)

## Installation

```bash
# Clone the repo
git clone https://github.com/your-username/Auto_Docstring_Generator.git
cd Auto_Docstring_Generator

# Install in editable mode (recommended for development)
pip install -e .
