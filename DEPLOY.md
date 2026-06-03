# Deploy to taiwofadoyin.co.uk

Your live site should be the contents of the **`site/`** folder (built by `python3 build-site.py`), not the project root.

## Option A — GitHub Pages (automatic from this repo)

Pushes to `main` deploy via GitHub Actions (see `.github/workflows/deploy.yml`).

1. [github.com/Fadoyin/mywebsite-portifolio/settings/pages](https://github.com/Fadoyin/mywebsite-portifolio/settings/pages) → **Source: GitHub Actions**.
2. Wait for the **Build and deploy to GitHub Pages** workflow to finish (Actions tab).
3. On the Pages settings page, set **Custom domain** → `taiwofadoyin.co.uk` → **Save** → enable **Enforce HTTPS** when offered.
4. **Google Workspace domain DNS** (Google Domains / Squarespace, or Admin → Domains):
   - GitHub will show required records after you add the custom domain.
   - For apex `taiwofadoyin.co.uk`, you typically add **four A records** pointing to GitHub Pages IPs (shown in the Pages UI), and optionally a **CNAME** for `www` → `fadoyin.github.io` (your Pages host).
5. DNS can take up to 24–48 hours; then visit **https://taiwofadoyin.co.uk**.

## Option B — Netlify (free SSL)

1. Create a free account at [netlify.com](https://www.netlify.com).
2. **Add new site → Deploy manually** (drag the `site` folder), **or** connect Git and set:
   - Build command: `python3 build-site.py`
   - Publish directory: `site`
   (already set in `netlify.toml` if you deploy from this folder.)
3. In Netlify: **Site configuration → Domain management → Add domain** → `taiwofadoyin.co.uk` and `www.taiwofadoyin.co.uk`.
4. At your domain registrar (where you bought `.co.uk`), set DNS as Netlify shows, typically:
   - **A** record for `@` → `75.2.60.5`
   - **CNAME** for `www` → your-site-name.netlify.app  
   Or use Netlify DNS (nameservers) for the whole domain.
5. Wait for DNS (minutes to 48 hours). Netlify provisions HTTPS automatically.

After deploy, open **https://taiwofadoyin.co.uk** — not localhost.

## Option C — Cloudflare Pages

1. [dash.cloudflare.com](https://dash.cloudflare.com) → **Workers & Pages** → Create → Pages → Upload `site` or connect Git.
2. Build: `python3 build-site.py`, output directory: `site`.
3. **Custom domains** → add `taiwofadoyin.co.uk`.
4. If the domain is already on Cloudflare, DNS is added for you.

## Option D — Any web host (cPanel, etc.)

1. Run `python3 build-site.py`.
2. Upload everything inside **`site/`** to `public_html` (or `www`).
3. Point domain **A** record to your host’s IP.
4. Enable SSL in the hosting panel (Let’s Encrypt).

## After you change designs

```bash
python3 build-site.py
```

Then redeploy (Netlify: drag `site` again, or push to Git if connected).

## Local testing with your domain name (optional)

This only works on **your Mac**, not for visitors:

```bash
# Add once (needs password):
sudo sh -c 'echo "127.0.0.1 taiwofadoyin.co.uk www.taiwofadoyin.co.uk" >> /etc/hosts'

cd site && python3 -m http.server 8080
# Open http://taiwofadoyin.co.uk:8080
```

For the real public site, use Option A/B/C — DNS + hosting — not `/etc/hosts`.
