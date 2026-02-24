# Automated Python Docstring Generator

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](.pre-commit-config.yaml)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-orange?logo=streamlit&logoColor=white)](https://streamlit.io/)

**A powerful, pip-installable tool** that automatically generates docstrings, analyzes documentation coverage, enforces PEP-257 compliance, and provides an interactive UI.

## Publish Documentation & Usage Guides

The **Automated Python Docstring Generator** is now fully documented, production-ready, and designed to be **developer-first**: easy to install, intuitive to use, and open for collaboration.

This section is your **single source of truth** — covering installation, CLI & UI usage, configuration, contribution guidelines, and real-world workflows.

### 1. Installation

Choose the method that fits your use case.

#### Option A: Quick Install from PyPI (recommended for most users)

```bash
pip install autodocstring-tool==0.1.0
Option B: Latest from GitHub Release (direct & no build needed)
Bashpip install https://github.com/keerthireddy2006/Automated-Python-Docstring-Generator/releases/download/v0.1.0/autodocstring_tool-0.1.0-py3-none-any.whl
Option C: Development / Editable Install (for contributors & testing)
Bashgit clone https://github.com/keerthireddy2006/Automated-Python-Docstring-Generator.git
cd Automated-Python-Docstring-Generator
pip install -e .
Quick Verification
Bashautodocstring --help
streamlit run app.py   # opens interactive UI
2. CLI Usage Examples
The CLI is powerful, flexible, and perfect for scripts, CI/CD, and batch processing.
Basic coverage check
Bashautodocstring calculator.py --style Google --verbose
autodocstring src/ --min-coverage 85 --verbose
Generate & apply docstrings
Bashautodocstring math_utils.py --style NumPy --apply --verbose
autodocstring legacy_code/ --style reST --apply --verbose
Run directly without install (dev mode)
Bashpython src/autodocstring/cli.py samples/ --style Google --min-coverage 90 --apply
CLI Flags Summary

FlagDescriptionDefaultExample--styleDocstring styleGoogle--style NumPy--min-coverageFail if any file below this %80.0--min-coverage 90--verboseDetailed per-file outputFalse--verbose--applyGenerate and inject docstringsFalse--apply
3. Configuration Guide
Configuration is currently flag-based (no separate config file yet — planned for v0.2).
Recommended team defaults

Style: Google (most readable)
Min coverage: 85–90% (quality enforcement)
Verbose: always in CI/CD pipelines

Future environment variables (planned)
Bashexport AUTODOC_DEFAULT_STYLE="NumPy"
export AUTODOC_MIN_COVERAGE=90
4. Contribution Guidelines
We actively welcome contributions — code, docs, issues, ideas!
How to Contribute

Fork the repository
Create your branch: git checkout -b feature/your-feature-name
Commit your changes: git commit -m 'Add your-feature-name'
Push: git push origin feature/your-feature-name
Open a Pull Request with clear title & description

Coding Standards (enforced via pre-commit)

Black formatting
PEP-257 compliant docstrings
Pytest coverage > 85%
Descriptive commit messages
No linting errors

Reporting Issues / Ideas

Use GitHub Issues
Include:
Steps to reproduce
Expected vs actual behavior
Screenshots
Python version & OS


Roadmap Ideas (community welcome)

VS Code / PyCharm extension
LLM-powered auto-fix suggestions
Coverage badge in README
PDF/CSV report export
Multi-language support

5. Example Workflows
Quick single-file fix
Bash# Check coverage
autodocstring my_module.py --verbose

# Generate & apply
autodocstring my_module.py --style Google --apply
Enforce team standards in CI/CD
Add to .github/workflows/ci.yml:
YAML- name: Enforce docstring coverage
  run: autodocstring src/ --min-coverage 90
Interactive editing session (UI)
Bashstreamlit run app.py
# Upload file → search missing → generate → apply → download updated file
Modernize legacy codebase
Bashautodocstring legacy_project/ --style NumPy --apply --verbose > coverage_report.txt
Development & testing cycle
Bashpip install -e .
pytest -v
streamlit run app.py
Final Note
Built with passion during the Infosys Springboard Internship.
Open-source, pip-installable, well-tested, and ready for real developers.
Thank you for exploring the documentation!
We welcome feedback, stars, forks, and contributions on GitHub.
Nkeerthi 



