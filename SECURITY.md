# Security

Cellwork is a static, client-side web page. It has no server, no accounts, no cookies and
no storage, and it makes no network requests. The realistic risks are therefore malicious
files a user opens in the app (an SVG outline, a density image or a project file) and the
third-party code bundled into the page.

## Reporting a vulnerability

Cellwork is maintained by Chris Spatschek.

Please use **GitHub's private vulnerability reporting** for this repository
(Security tab → *Report a vulnerability*) rather than a public issue. Include the browser,
steps to reproduce and, if possible, the file that triggers the problem.

## Protections in place

| Area | Measure |
|---|---|
| Script injection | Content Security Policy with `default-src 'none'` and SHA-256 hashes for the app's own inline script and style blocks. No `eval`, no `new Function`, no inline event handlers. |
| Network and privacy | `connect-src 'none'`; no external fonts, scripts or images. The font is embedded, so no request goes to Google or any CDN. `referrer` is set to `no-referrer`. |
| Imported SVG outlines | Never inserted as-is. The file is parsed with `DOMParser`, then only geometry elements (`svg`, `g`, `path`, `rect`, `circle`, `ellipse`, `polygon`, `polyline`) and geometry attributes are copied into new elements. Scripts, event handlers, links, `<image>`, `<use>`, `<foreignObject>`, styles and `url(...)` references are dropped. Size and element-count limits apply. |
| Project files (`.json`) | Every setting is checked against the expected type and range and against fixed lists of allowed values; unknown keys are ignored, so there is no prototype pollution. Points, mounting holes, painted areas and outlines are validated and capped in size. |
| Markup built from data | Text from files (for example image file names) is written with `textContent`. The few places that build markup interpolate only numbers. |
| Denial of service | File size limits (SVG 15 MB, image 40 MB, project 50 MB), at most 8,000 cells, capped outline sampling and PNG size. Very heavy settings can still make the tab slow, but only on the user's own device. |
| Third-party code | d3-delaunay 6.0.4 and Clipper JS 6.4.2 are vendored at exact versions with recorded SHA-256 hashes (`vendor/README.md`). Both only do geometry and touch neither the DOM nor the network. |

## Known limitations

- GitHub Pages cannot send HTTP headers, so `frame-ancestors` (clickjacking protection) cannot
  be enforced from a `<meta>` tag. The impact is low: the page has no login and no actions on
  other sites. If you host Cellwork elsewhere, add the header
  `Content-Security-Policy: frame-ancestors 'none'` and `X-Content-Type-Options: nosniff`.
- When an imported SVG contains `style` attributes, the browser logs a CSP violation while
  parsing it. That message means the style was blocked, as intended.
- Exported files are plain data (SVG paths, DXF polylines, PNG, JSON). They contain no
  scripts, but always review cut files in your machine software before running a job.
