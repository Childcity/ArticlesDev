# ArticlesDev

This repository stores papers in `papers/` and includes a script to convert the source documents into UTF-8 LaTeX files. The generated documents use **XeLaTeX** for Ukrainian, other Unicode text, and formulas.

## Install for local Windows use

Install:

- **Python 3.11 or newer**
- **MiKTeX**, including the XeLaTeX engine; the script detects the standard Windows install path, or you can add its `miktex\bin\x64` directory to `PATH`
- **7-Zip** and add its installation folder to `PATH` if you need to convert legacy `.doc` files

In MiKTeX, allow it to install missing packages when prompted. The documents use `fontspec`, `polyglossia`, `amsmath`, `amssymb`, `geometry`, `graphicx`, and the TeX Gyre Termes font (`tex-gyre` MiKTeX package).

Set up the Python environment from the repository root:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r src\requirements-papers-to-latex.txt
```

Generate or regenerate the LaTeX files:

```powershell
.venv\Scripts\python.exe src\papers_to_latex.py papers
```

To generate and compile them with XeLaTeX:

```powershell
.venv\Scripts\python.exe src\papers_to_latex.py papers --compile
```

For a book or proceedings folder, pass the article title if automatic title matching selects the wrong article:

```powershell
.venv\Scripts\python.exe src\papers_to_latex.py papers --paper-title "Folder_Name=Article Title"
```

## Install for Codex Cloud

Codex Cloud tasks use a separate remote environment; they cannot use MiKTeX or other programs installed on your PC. When creating the Codex Cloud environment for this GitHub repository, ask Codex to install and verify **TeX Live with XeLaTeX**. Codex Cloud saves the tested install script with the published environment, and new cloud tasks start from that setup.

For a Debian/Ubuntu-based environment, install these system packages:

```bash
apt-get update
apt-get install -y \
  python3 python3-venv \
  p7zip-full \
  texlive-xetex texlive-latex-recommended texlive-latex-extra texlive-lang-cyrillic \
  fonts-texgyre
```

If the cloud task will regenerate papers from DOCX/PDF/DOC sources, also install the Python dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r src/requirements-papers-to-latex.txt
```

Then verify the compiler is available:

```bash
xelatex --version
.venv/bin/python src/papers_to_latex.py papers --compile
```

Enable package-manager internet access during Codex Cloud environment setup so the system packages can be downloaded. After Codex tests the setup, review and publish the environment. If you only plan to edit and compile existing `.tex` files in the cloud, the XeLaTeX/TeX Live packages are the essential part; Python and 7-Zip are only needed to regenerate them from the original files.

## Converter details

See [the converter guide](src/README_papers_to_latex.md) for supported formats and reusable command-line options. An empty folder receives a small placeholder `.tex` file so the folder still has a compilable LaTeX document.
