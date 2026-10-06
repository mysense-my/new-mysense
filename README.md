# MYSense website revamp (Velora layout)

Static rebuild of mysense.com.my on the Velora Framer template design, in MYSense colours (navy / purple), Montserrat + Poppins, using the copy and media of the current site.

- `site/` — the generated website (63 pages). Open `site/index.html` or serve the folder with any static server.
- `build/` — the generator. `python3 build/gen.py` rebuilds `site/` from `build/gen.py`, `build/gen_pages.py`, `build/components.py`, `build/src/main.css` and `build/src/main.js`.

Forms are mock-ups (the HubSpot forms still need to be embedded). All page links are relative, so the site also works from a sub-path such as GitHub Pages.
