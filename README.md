# Automated Python Docstring Generator

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](.pre-commit-config.yaml)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-orange?logo=streamlit&logoColor=white)](https://streamlit.io/)

**A powerful, pip-installable tool** that automatically generates docstrings, analyzes documentation coverage, enforces PEP-257 compliance, and provides an interactive UI.

```markdown
## Publish Documentation & Usage Guides

The **Automated Python Docstring Generator** is fully documented, production-ready, and built to be **developer-first** — simple to install, powerful to use, and open for contributions.

This section is your **complete guide** — from installation to advanced workflows.

### 1. Installation

#### Option A: Quick Install from PyPI (recommended)

```bash
pip install autodocstring-tool==0.1.0
```

#### Option B: Direct from GitHub Release

```bash
pip install https://github.com/keerthireddy2006/Automated-Python-Docstring-Generator/releases/download/v0.1.0/autodocstring_tool-0.1.0-py3-none-any.whl
```

#### Option C: Development / Editable Install

```bash
git clone https://github.com/keerthireddy2006/Automated-Python-Docstring-Generator.git
cd Automated-Python-Docstring-Generator
pip install -e .
```

**Quick check after install**

```bash
autodocstring --help
streamlit run app.py   # opens interactive UI
```

### 2. CLI Usage Examples

**Coverage check**

```bash
# Single file
autodocstring calculator.py --style Google --verbose

# Entire folder
autodocstring src/ --min-coverage 85 --verbose
```

**Generate & apply docstrings**

```bash
# Single file
autodocstring math_utils.py --style NumPy --apply --verbose

# Batch apply
autodocstring legacy/ --style reST --apply --verbose
```

**Run directly (no install needed)**

```bash
python src/autodocstring/cli.py samples/ --style Google --min-coverage 90 --apply
```

**CLI Flags Overview**

| Flag               | Description                                      | Default   | Example                     |
|--------------------|--------------------------------------------------|-----------|-----------------------------|
| `--style`          | Docstring style                                  | Google    | `--style NumPy`             |
| `--min-coverage`   | Fail if any file below this %                    | 80.0      | `--min-coverage 90`         |
| `--verbose`        | Detailed per-file output                         | False     | `--verbose`                 |
| `--apply`          | Generate and inject docstrings                   | False     | `--apply`                   |

### 3. Configuration Guide

Configuration is currently **flag-based** (no separate config file yet — planned for v0.2).

**Recommended defaults for teams**

- Style: Google (most readable)
- Min coverage: 85–90% (quality gate)
- Verbose: always in CI/CD

**Future environment variables** (planned)

```bash
export AUTODOC_DEFAULT_STYLE="NumPy"
export AUTODOC_MIN_COVERAGE=90
```

### 4. Contribution Guidelines

We welcome contributions — bug fixes, features, docs, or ideas!

**How to Contribute**

1. Fork the repository
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'Add your-feature-name'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request with clear title & description

**Coding Standards** (enforced via pre-commit)

- Black formatting
- PEP-257 compliant docstrings
- Pytest coverage > 85%
- Descriptive commit messages
- No linting errors

**Reporting Issues**

- Use GitHub Issues
- Include: steps to reproduce, expected vs actual, screenshots, Python version

**Roadmap Ideas** (open for contributions)

- VS Code / PyCharm extension
- LLM auto-fix suggestions
- Coverage badge in README
- PDF/CSV report export
- Multi-language support

### 5. Example Workflows

**Quick single-file fix**

```bash
autodocstring my_module.py --verbose
autodocstring my_module.py --style Google --apply
```

**Enforce team standards in CI**

Add to `.github/workflows/ci.yml`:

```yaml
- name: Enforce docstring coverage
  run: autodocstring src/ --min-coverage 90
```

**Interactive session (UI)**

```bash
streamlit run app.py
# Upload → search missing → generate → apply → download
```

**Modernize legacy codebase**

```bash
autodocstring legacy_project/ --style NumPy --apply --verbose > coverage_report.txt
```

**Development & testing cycle**

```bash
pip install -e .
pytest -v
streamlit run app.py
```

### Final Note

Built with passion during the Infosys Springboard Internship.
Open-source, pip-installable, well-tested, and ready for real developers.

**Thank you** for reading!
We welcome feedback, stars, forks, and contributions.

Nkeerthi
[GitHub Repository](https://github.com/keerthireddy2006/Automated-Python-Docstring-Generator)
[Report Issues](https://github.com/keerthireddy2006/Automated-Python-Docstring-Generator/issues)
```
