# ForWARD Lab website

Static site for the **ForWARD Lab: For Wellbeing And Resilience in Development** (PI: Jamie Hanson, Department of Pediatrics, Medical College of Wisconsin and Children's Wisconsin).

Plain HTML, CSS, and a small vanilla JS file. No framework, no build step. The only external dependency is Google Fonts (Source Serif 4 and Source Sans 3).

## Files

```
index.html          Home: tagline, affiliations, six section cards
research.html       Mission, 4 focus areas, PI bio and headshot
team.html           PI, lab alumni with current positions, collaborators
publications.html   10 selected papers + all 92 (generated from the CV)
participate.html    For families: what studies involve, privacy, how to reach us
news.html           Dated news items
funding.html        Current and recent grants (footer + Research link, not in nav)
contact.html        Contact info, email button, how to join the lab
css/styles.css      All styles; brand colors at the top in :root
js/main.js          Mobile nav, footer year, hero pause button, form validation (for future forms)
assets/img/         forward-logo-blue.svg / forward-logo-white.svg (logo), favicon.svg,
                    hero-brain-1/2.svg (home hero rotation), hanson-portrait/square.webp,
                    people/ (alumni and collaborator photos)
tests/check_site.py Static checks (links, alt text, nav, labels, contrast, pubs)
tools/update_publications.py   Rebuilds the publication list from the CV
tools/doi_cache.json           Crossref DOI matches (keeps reruns fast and stable)
tools/stamp_assets.py          Cache-busting ?v= stamps on CSS/JS links (run before pushing)
tools/logo/build_logo.py       Builds the logo and favicon SVGs
tools/logo/banner_tracts.py    Draws the logo's converging tracts in every page banner
tools/add_people_photos.py     Adds photos from photos-inbox/ to People page cards (alumni and collaborators)
tools/hero_art/                Scripts that build the hero art from the MNI152 template
```

## Preview locally

Open `index.html` in a browser, or run a local server (better, since it matches how the site is hosted):

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000.

## Update publications from your CV

```bash
python3 tools/update_publications.py ~/Library/CloudStorage/Dropbox/CV_Resume_mostUptoDate/Hanson_CV_YYYYMMDD.docx
```

Reads the "Peer-Reviewed Journal Articles", "Book Chapters", and "Journal Commentaries" sections (skips "Manuscripts Under Review"), fills missing DOIs from Crossref (only title matches of 90% or better, never preprint-server DOIs), and rewrites only the block between `<!-- PUBS:START -->` and `<!-- PUBS:END -->` in `publications.html`. To change the selected papers or their group labels, edit `SELECTED` at the top of the script. DOIs checked by hand live in `DOI_OVERRIDES`. The script prints any article still missing a link.

## Check before publishing

```bash
python3 tests/check_site.py
```

Fails on: broken local links or anchors, images without `alt`, pages without exactly one `<h1>`, nav that differs across pages, form fields without labels, external assets other than Google Fonts, em dashes, and any brand color pair below WCAG AA (4.5:1). It also prints how many `PLACEHOLDER` markers remain. Rerun it after changing colors.

## Hosting

- **Live:** https://forwardlab-mke.com/ (www redirects to it). HTTPS is enforced, and the certificate covers both names.
- **Repo:** https://github.com/forwardlab-mke/forwardlab-mke.github.io (GitHub Pages, branch `main`, folder `/`). The `CNAME` file holds the domain; don't delete it.
- **DNS (Porkbun):** `A` records for `@` to 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `CNAME` `www` to `forwardlab-mke.github.io`. Leave Porkbun URL forwarding off; it can override these records.

This site started as a copy of the TaLE MKE site (`~/tale-mke-site`, live at tale-mke.com) with its own git history.

To publish a change: edit, check, commit, push. GitHub rebuilds in about a minute.

```bash
python3 tools/stamp_assets.py && python3 tests/check_site.py && git add -A && git commit -m "Describe the change" && git push
```

`tools/stamp_assets.py` adds a content hash to the CSS and JS links (`styles.css?v=...`). GitHub Pages lets browsers cache files for 10 minutes; the stamp makes browsers fetch a changed stylesheet or script right away instead of pairing new HTML with an old cached file. The check script fails if a stamp is stale.

Commits should use the GitHub noreply address (`git config user.email`), so no personal email shows in the public history. `.nojekyll` tells GitHub to serve the files as they are.

To use a custom domain later (e.g. a lab domain), add it under repo Settings > Pages > Custom domain and create the DNS record GitHub shows you.

## What still needs you

| What | Where |
|---|---|
| Home hero image | `index.html` crossfades two brain illustrations (`hero-brain-1.svg`, `hero-brain-2.svg`) and the logo slide (`hero-logo.svg`, built by `tools/logo/build_logo.py`), 6s each, pause button, still for reduced-motion users) with no logo overlay for now. The brain comes from the MNI152 template; see `tools/hero_art/README.md` to rebuild or restyle. With no logo overlay (`LOGO_OVERLAY = False` in `hero_variants.py`) the drawings are centered. To use a lab group photo instead, replace the `<figure class="hero-art">` with one `<img>` (4:3, 1200x900 or larger) and write its `alt`. |
| Payment wording on Participate | `participate.html`, marked `CONFIRM`. It says studies "often include payment"; confirm before launch. |

### Brand

**Logo.** The mark is design "E3, Denser Tracts with green flow": an outline brain (MNI152 template, facing right) where nine tracts start at nodes that grow toward the front, turn MCW green as they converge, and continue as a see-through arrow. Files in `assets/img/`, all generated by `tools/logo/build_logo.py` (edit the script, not the SVGs):

- `forward-logo-blue.svg`: for blue backgrounds (site header and footer); the arrow uses a light mint so it stays visible on blue
- `forward-logo-white.svg`: for white backgrounds (documents, slides, posters)
- `hero-logo.svg`: the logo as the third home-page hero slide
- `favicon.svg`: browser-tab icon, a simplified version (no folds, bolder lines) on a blue square so it reads at 16 to 32 px

**Banner graphic.** Each page banner has a faint decorative graphic of the logo's converging tracts (blue to green on the light inner-page banners, white to mint on the blue home hero). It is drawn inline in each page by `tools/logo/banner_tracts.py`; rerun that script after editing it.

The wordmark ("**For**WARD Lab" with "For Wellbeing And Resilience in Development" beneath) is live text styled in `css/styles.css` (`.wordmark`).

**Slogans in use:** "Helping kids move forward." (home hero), "Forward from the start." (Research mission), "Moving Milwaukee kids forward." (Participate banner), "Forward for Wisconsin." (footer).

**Colors** live at the top of `css/styles.css` and carry over from the TaLE MKE palette:

| Token | Hex | Used for |
|---|---|---|
| `--color-primary` | `#0074c8` | Blue: header, home hero, footer, buttons, links |
| `--color-primary-dark` | `#005a9c` | Hover states; blue text on pale-blue surfaces |
| `--color-secondary` | `#007065` | MCW green (mcw.edu uses #007066): header/footer bars, nav outlines, accents |
| `--color-accent-light` | `#7eb8e0` | Light-blue lines |
| `--color-accent-pale` | `#c1ddf4` | Pale-blue lines |

Logo blue on white is 4.85:1 (passes AA); logo blue on pale blue does not, so text on pale-blue surfaces uses `--color-primary-dark`. `tests/check_site.py` enforces this and fails on any leftover TaLE MKE branding.

### Contact

`contact.html` uses an email button (`mailto:jamhanson@mcw.edu`) in place of a form, so there is no form service to run. The form-validation code in `js/main.js` is kept: any `<form class="js-form">` added later (for example a family sign-up on `participate.html`) gets validation automatically, and `FORM_ENDPOINT` is where a handler such as Formspree or REDCap would go. Check with MCW/Children's Wisconsin research compliance before collecting families' contact details.

### People photos

1. Save photos in `photos-inbox/` (create it if needed; it is never published) named after the person exactly as on the People page (alumni or collaborators), e.g. `Kelly Barry.jpg`. Accents are optional. JPG, PNG, WebP and iPhone HEIC all work.
2. Run `python3 tools/add_people_photos.py`. Each photo is square-cropped (centered, favoring the top of the frame), resized to 320x320, saved to `assets/img/people/` with EXIF/GPS metadata removed, and swapped into that person's card in place of the initials.
3. Check the People page, then publish as usual.

The script lists anyone still showing initials and any photo whose name matched no one. Ask people before posting their photo.

### Photos

Use JPG or WebP. Suggested sizes: headshots square, 600x600 or larger; lab photo 4:3, 1200x900 or larger. Always write an `alt` that describes the person or scene.

### Editing the shared header and footer

The header and footer are repeated in each of the 8 HTML files (no build step). When you change one, change all eight. `tests/check_site.py` catches nav drift.
