# ArticlesDev

This repository contains research papers and a converter that creates UTF-8 LaTeX files from source documents in `papers/`. Generated documents support Ukrainian and other Unicode text and should be compiled with XeLaTeX.

## Set up on Debian 13 (Codex Cloud)

From the repository root, install the system tools and Python dependencies:

```bash
cd /workspace/ArticlesDev

. /etc/os-release
apt_sources="$(mktemp)"
trap 'rm -f "$apt_sources"' EXIT
cat >"$apt_sources" <<EOF
deb https://deb.debian.org/debian ${VERSION_CODENAME} main
deb https://deb.debian.org/debian-security ${VERSION_CODENAME}-security main
EOF

apt-get -o Dir::Etc::sourcelist="$apt_sources" \
  -o Dir::Etc::sourceparts=- -o APT::Get::List-Cleanup=0 update
apt-get -o Dir::Etc::sourcelist="$apt_sources" -o Dir::Etc::sourceparts=- \
  install -y python3 python3-venv p7zip-full \
  texlive-xetex texlive-latex-recommended texlive-latex-extra \
  texlive-lang-cyrillic fonts-texgyre

python3 -m venv .venv
.venv/bin/python -m pip install -r src/requirements-papers-to-latex.txt
```

The explicit Debian mirrors are useful in cloud images whose configured APT snapshot host is blocked by the network proxy. APT keeps its normal repository signature and TLS verification enabled. System packages require an environment with permission to install them.

Check the tools:

```bash
.venv/bin/python -m pip check
7z
xelatex --version
```

## Convert and compile papers

Each immediate subfolder of `papers/` produces one `.tex` file. DOCX and PDF input use the Python dependencies; legacy DOC input also requires 7-Zip.

```bash
.venv/bin/python src/papers_to_latex.py papers
```

Compile the generated LaTeX with XeLaTeX:

```bash
.venv/bin/python src/papers_to_latex.py papers --compile
```

The converter writes `.tex` files and, with `--compile`, `.pdf` files into the paper folders. For a book or proceedings folder where automatic title selection is ambiguous, specify a title:

```bash
.venv/bin/python src/papers_to_latex.py papers --paper-title "Folder_Name=Article Title"
```

See [the converter guide](src/README_papers_to_latex.md) for supported formats and additional options.
