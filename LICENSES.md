# Licences

## PyBook itself

MIT License

Copyright (c) 2026 PyBook contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Third-party code

The **notebook** imports only the Python standard library (`json`, `pathlib`,
`datetime`, `random`, `statistics`, `collections`, `itertools`, `functools`,
`csv`, `io`, `asyncio`, `unittest`, `dataclasses`, `contextlib`, `traceback`,
`html`, `os`, `sys`, `types`, `importlib`). Nothing is vendored into it.

The **web platform** ships the libraries below inside `web/static/vendor/`, so
the site makes no third-party request at runtime. Each entry is the licence of
the exact file in this repository.

| Component | Version | Licence | Used for |
|---|---|---|---|
| Flask | 3.1.3 | BSD-3-Clause | HTTP routing, templates, sessions |
| Werkzeug | 3.1.x | BSD-3-Clause | Password hashing, request/response plumbing |
| waitress | 3.0.2 | ZPL-2.1 | Production WSGI server (`python run.py`) |
| Alpine.js | 3.14.9 | MIT | Interactive lesson widgets, drills, quiz state |
| GSAP | 3.13.0 | GreenSock Standard "No Charge" Licence | Page and progress animations |
| Prism | 1.29.0 | MIT | Syntax highlighting in static code blocks |
| CodeMirror | 5.65.19 | MIT | The code editor in lessons and the playground |
| Chart.js | 4.4.7 | MIT | Progress and admin charts |
| canvas-confetti | 1.9.3 | ISC | Lesson-complete celebration |
| Inter | variable | SIL OFL 1.1 | Interface typeface |
| JetBrains Mono | 400, 700 | SIL OFL 1.1 | Code typeface |

Notes, stated plainly:

- **GSAP** is free to use under GreenSock's own standard licence, which is not an
  OSI licence. If you republish or sell this project, read
  <https://gsap.com/standard-license> and confirm your use is covered; swapping
  it for a CSS-only animation is a drop-in alternative, since every animation
  here is decorative.
- The two fonts are redistributed under the SIL Open Font Licence 1.1, which
  permits bundling; the font files are unmodified.
- Every other library above is permissively licensed and compatible with this
  project's MIT licence.

The test suite uses `pytest` and `nbformat`, which are development-only
dependencies and are not shipped inside the notebook or the web app.

## Images and diagrams

All 16 diagrams in `course/visuals.py` are **original SVG** written for this
project: plain `<svg>` markup with CSS keyframes, no external fonts, no raster
images, no icon packs. They are covered by the MIT licence above, so there is
nothing else to attribute and nothing to download at runtime.

No emoji artwork is bundled: the emoji in headings are Unicode characters
rendered by the reader's own font.

## Content and sources

The curriculum follows the structure of the official Python documentation:

- The Python Tutorial — <https://docs.python.org/3/tutorial/>
- The Python Language Reference — <https://docs.python.org/3/reference/>
- The Python Standard Library — <https://docs.python.org/3/library/>

Those pages are © the Python Software Foundation, licensed under the PSF
License Agreement. PyBook does not copy their text: each lesson links to the
relevant page and explains the idea in its own words, in English, Hindi and
Hinglish.

Python itself is distributed under the PSF License Agreement; this project only
teaches it and does not redistribute the interpreter.

## What is deliberately not here

- No copied lesson text, exercises or diagrams from other courses.
- No scraped question banks.
- No paid asset packs, no "free for non-commercial use" assets, and no
  attribution-required stock imagery.
