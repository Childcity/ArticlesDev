# Papers to XeLaTeX

Create one UTF-8 `.tex` file per immediate subfolder of `papers`. DOCX files
are read with `python-docx`; PDFs are extracted with `pypdf`. Legacy DOC files
are read from their Word document stream using 7-Zip (installed automatically
from the standard Program Files location on Windows, or available on `PATH`).
Equations and mathematical symbols are retained as text where the source
format exposes them; the converter does not recreate diagrams or page layout.

## Setup

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r src\requirements-papers-to-latex.txt
```

## Run

```powershell
.venv\Scripts\python.exe src\papers_to_latex.py papers
```

Replace spaces in folder names first:

```powershell
.venv\Scripts\python.exe src\papers_to_latex.py papers --normalize-folder-names
```

For a book or proceedings PDF, the converter uses the folder and `цитата.txt`
as the article title hint. Supply an explicit title when that is ambiguous:

```powershell
.venv\Scripts\python.exe src\papers_to_latex.py papers --paper-title "Folder_Name=Article Title"
```

Compile generated files with XeLaTeX installed and on `PATH`:

```powershell
.venv\Scripts\python.exe src\papers_to_latex.py papers --compile
```

Each TeX file uses `fontspec` and `polyglossia`, so compile with XeLaTeX.
