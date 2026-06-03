# Taiwo Fadoyin — Portfolio

Personal portfolio site for [taiwofadoyin.co.uk](https://taiwofadoyin.co.uk).

## Build

```bash
python3 build-site.py
```

Output is in `site/` — deploy that folder (see `DEPLOY.md`).

## Deploy (GitHub Actions → GitHub Pages)

Every push to `main` runs [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml): builds the site and publishes `site/` to GitHub Pages.

**One-time setup:**

1. Open [repo Settings → Pages](https://github.com/Fadoyin/mywebsite-portifolio/settings/pages).
2. **Build and deployment → Source:** choose **GitHub Actions** (not “Deploy from a branch”).
3. After the first workflow run succeeds, set **Custom domain** to `taiwofadoyin.co.uk` and enable **Enforce HTTPS**.
4. In **Google Workspace / domain DNS**, add the records GitHub shows (for apex `.co.uk`, usually **A** records to GitHub’s IPs, or follow GitHub’s custom-domain wizard).

Live URL after DNS propagates: **https://taiwofadoyin.co.uk**

## Stack

Static HTML + Tailwind (CDN). Source designs exported from Google Stitch.
