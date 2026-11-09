# Vendored libraries

These files are inlined into `index.html` by `build.py`. They are pinned to exact
versions and checked in, so the app never loads code from a CDN at runtime.

| File | Source | Upstream package SHA-256 (npm tarball) |
|---|---|---|
| `d3-delaunay.min.js` | `d3-delaunay@6.0.4`, file `dist/d3-delaunay.min.js`, unchanged | `935113ffa78d545505c8f1accf95be0e48594737eab34db8f50c9d6319907971` |
| `clipper.min.js` | `clipper-lib@6.4.2`, file `clipper.js`: original licence header (lines 1–65) followed by the file minified with `terser -c -m` | `634d7d7627939bbe63405f8876c43ba4009b1fec7ef8de153b0bed28e42466ec` |
| `../fonts/InstrumentSans-latin.woff2` | Instrument Sans variable TTF from `google/fonts` (`ofl/instrumentsans`), instanced to wdth 100 / wght 400–700 and subset to Latin with fontTools (name IDs 0–6, 13, 14 kept, so copyright and licence metadata stay in the font) | – |

SHA-256 of the files as committed:

```
efc726aa8aea0897f6dda19874709d09fd791781208ed5847ef1fd36f9886b18  vendor/d3-delaunay.min.js
e3a2a7fec23d0553e28ed82ea94e4fc9c7994e256fd5064685f65ccf702bf636  vendor/clipper.min.js
922cda9259e266cb495bf5c872fbc303ccc2039e0572f70726cdf273f0837995  fonts/InstrumentSans-latin.woff2
```

## Updating

1. `npm pack <package>@<version>` and check the tarball hash against the npm registry's `integrity` field.
2. Replace the file here, rebuild with `python3 build.py` and test every export.
3. Update the version and hashes above and in `THIRD_PARTY_NOTICES.md`.

Both libraries are mature and have no runtime network or DOM access; they only do geometry.
