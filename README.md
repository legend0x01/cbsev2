# NCERT Notes — Make Study Better

A fast, single-page study site with concise, colourful NCERT chapter notes for **CBSE Classes 9–12**, plus a Python tool that builds printable PDF notes for every chapter.

![NCERT Notes home page](screenshots/home.png)

## Features

- **Classes 9, 10, 11 and 12** — switch class with one tap
- **Subject filters** — Physics, Chemistry, Biology, Mathematics and more
- **Chapter cards** — key topics, read time and tags such as *High Weightage* and *Board Essential*
- **Built-in reader** — revision notes, formulas and cheat-sheets for each chapter
- **Search** — find a chapter, formula or topic instantly
- **One-click printable PDFs**
- **Dark mode and Night Light** for comfortable reading, with preferences saved in your browser
- **Responsive** — works on phones, tablets and desktops

## Tech stack

- **Website:** one `index.html` file using HTML, Tailwind CSS and vanilla JavaScript, with no build step
- **PDF generator:** Python 3 with `requests`, `BeautifulSoup` and `fpdf`

## Getting started

### Website

Open `index.html` in any browser, or serve the folder locally:

```bash
git clone https://github.com/legend0x01/cbsev2.git
cd cbsev2
python -m http.server 8000   # then visit http://localhost:8000
```

### PDF notes generator

`generate_ncert_pdfs.py` covers the full NCERT syllabus for Classes 9–12. It gathers notes for each chapter from public study sites and writes one PDF per chapter, organised by class and subject.

```bash
pip install requests beautifulsoup4 fpdf
python generate_ncert_pdfs.py
```

> Notes fetched from third-party sites belong to their owners. Use the generated PDFs for personal study only.

## License

Released under the [MIT License](LICENSE).
