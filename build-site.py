#!/usr/bin/env python3
"""Assemble Stitch HTML exports into a linked multi-page portfolio."""

from pathlib import Path
import hashlib
import re
import shutil
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"

PAGES = [
    ("index.html", "home_hero/code.html", "Home"),
    ("about.html", "about_taiwo_fadoyin_cleaned_up/code.html", "About"),
    ("work.html", "work_taiwo_fadoyin_cleaned_up/code.html", "Work"),
    ("services.html", "services_taiwo_fadoyin_cleaned_up/code.html", "Services"),
    ("blog.html", "blog_taiwo_fadoyin_cleaned_up/code.html", "Blog"),
    ("contact.html", "contact_taiwo_fadoyin_cleaned_up/code.html", "Contact"),
]

NAV_LABELS = ("Home", "About", "Work", "Services", "Blog")
NAV_FILES = {
    "Home": "index.html",
    "About": "about.html",
    "Work": "work.html",
    "Services": "services.html",
    "Blog": "blog.html",
}

DRAWER_ICONS = {
    "home": "index.html",
    "person": "about.html",
    "work": "work.html",
    "terminal": "services.html",
    "article": "blog.html",
}

ACTIVE_CLASS = (
    "text-primary-fixed-dim font-bold border-b border-primary-fixed-dim pb-1"
)
INACTIVE_CLASS = (
    "text-on-surface-variant font-medium hover:text-primary-fixed-dim "
    "transition-colors duration-200"
)

# Private Stitch URLs often fail in the browser; use the public portrait export.
PORTRAIT_PRIVATE = (
    "https://lh3.googleusercontent.com/aida/AP1WRLssrvhvmk3yG8tTIyRdGn2qxU8f2vPtu8M8jqW7QJUr-5kz24KHBGxqV5umKC25z77NO8AvpIzDsfcEhHJk4_UmYWKvEE8llZdfpxzG7tYhaAjxPEdkIH05qK2ewErq0m1pQEQ3T9KHx2QQZv-IOADbHOwN4XcpxFcCpW5YOzEnt2oc2vv697aWQzhsQEiVL669PRyIzG_tWnYzazEH1KsIfdo75tqdJ6A7e_zNbcZHaswz09waQNUv_xvY"
)
PORTRAIT_PUBLIC = (
    "https://lh3.googleusercontent.com/aida-public/AB6AXuDuSlF7MCnuizWG_RZqtn6eYbBnAPi1ro6SP71XYkw0W34N47LEP2RcLVa-kVe6NYm2t9qk832oiCkt-obkBMs97YGMIw6ZY2AAUwmYe0BDVKMzJRLz8JbLXc9FRqxoXIkaukumTH7F6UC6N77KDSiJg05vr_r4iq2h1Hpv55pZCnGEsf010mKC41NMRJyVk2xeHAq5l-rak2_5ZG91FxldWg1AmAj7CFQmVetECrzwXU0BSMWQeAzSZsaIIDP4Ytj2AUlTLBltFF-X"
)

LOCAL_PORTRAIT = (
    ROOT
    / "a_high_quality_professional_black_and_white_portrait_of_the_person_in_data"
    / "screen.png"
)

DOMAIN = "taiwofadoyin.co.uk"
SITE_URL = f"https://{DOMAIN}"
EMAIL = f"contact@{DOMAIN}"
LINKEDIN = "https://www.linkedin.com/in/taiwo-fadoyin-119726209/"

PAGE_TITLES = {
    "index.html": f"Taiwo Fadoyin — Full-stack Developer | {DOMAIN}",
    "about.html": f"About | Taiwo Fadoyin",
    "work.html": f"Work | Taiwo Fadoyin",
    "services.html": f"Services | Taiwo Fadoyin",
    "blog.html": f"Blog | Taiwo Fadoyin",
    "contact.html": f"Contact | Taiwo Fadoyin",
}

IMAGE_URL_KEYS = (
    ("AB6AXuDuSlF7MCnuizWG", "portrait.png"),
    ("AB6AXuB8pcmmO2eIrqq2", "work-ledgerly.png"),
    ("AB6AXuCmU199N0Km5LxO", "work-paybridge.png"),
    ("AB6AXuDtMAlpzmiTbJxGD", "work-roomly.png"),
    ("AB6AXuD46FxaL200WAvu52", "work-envcheck.png"),
    ("AB6AXuCKsPY0MxQobq6OJ", "blog-featured.png"),
    ("AB6AXuCc0IJ-cC9f8UwZq8", "services-workspace.png"),
)


def replace_nav_hrefs(html: str) -> str:
    for label, target in NAV_FILES.items():
        html = html.replace(f'href="#">{label}', f'href="{target}">{label}')
        html = html.replace(f'href="#{label.lower()}">{label}', f'href="{target}">{label}')
    for anchor, target in (
        ("#home", "index.html"),
        ("#about", "about.html"),
        ("#work", "work.html"),
        ("#services", "services.html"),
        ("#blog", "blog.html"),
    ):
        html = html.replace(f'href="{anchor}"', f'href="{target}"')
    return html


def fix_drawer_icon_links(html: str) -> str:
    for icon, target in DRAWER_ICONS.items():
        html = re.sub(
            rf'href="#"(>\s*<span class="material-symbols-outlined"[^>]*>{icon}</span>)',
            f'href="{target}"\\1',
            html,
        )
    return html


def brand_link(html: str) -> str:
    html = re.sub(
        r'<div class="font-display-xl-mobile text-body-md font-bold text-on-surface flex items-center gap-2(?: after:[^"]*)?">\s*Taiwo Fadoyin\s*'
        r'(<span class="w-2 h-2 bg-primary-fixed-dim rounded-full animate-pulse"></span>)\s*</div>',
        r'<a href="index.html" class="font-display-xl-mobile text-body-md font-bold text-on-surface '
        r'flex items-center gap-2 hover:text-primary-fixed-dim transition-colors">\n            '
        r'Taiwo Fadoyin\n            \1\n</a>',
        html,
        count=1,
    )
    html = re.sub(
        r'<div class="font-display-xl-mobile text-body-md font-bold text-on-surface flex items-center gap-2 after:content-\[[^\]]+\][^"]*">Taiwo Fadoyin</div>',
        '<a href="index.html" class="font-display-xl-mobile text-body-md font-bold text-on-surface '
        'flex items-center gap-2 hover:text-primary-fixed-dim transition-colors">Taiwo Fadoyin</a>',
        html,
        count=1,
    )
    html = re.sub(
        r'<a class="font-display-xl-mobile[^"]*" href="#">Taiwo Fadoyin</a>',
        '<a class="font-display-xl-mobile text-body-md font-bold text-on-surface flex items-center gap-2 '
        'hover:text-primary-fixed-dim transition-colors" href="index.html">Taiwo Fadoyin</a>',
        html,
        count=1,
    )
    html = re.sub(
        r'(<div class="p-6[^"]*flex justify-between[^"]*">\s*)'
        r'<span class="font-display-xl-mobile text-headline-lg font-bold text-on-surface">Taiwo Fadoyin</span>',
        r'\1<a href="index.html" class="font-display-xl-mobile text-headline-lg font-bold text-on-surface '
        r'hover:text-primary-fixed-dim transition-colors">Taiwo Fadoyin</a>',
        html,
        count=1,
    )
    html = re.sub(
        r'(<div class="flex justify-between items-center mb-12">\s*)'
        r'<span class="font-display-xl-mobile text-headline-lg font-bold text-on-surface">Taiwo Fadoyin</span>',
        r'\1<a href="index.html" class="font-display-xl-mobile text-headline-lg font-bold text-on-surface '
        r'hover:text-primary-fixed-dim transition-colors">Taiwo Fadoyin</a>',
        html,
        count=1,
    )
    html = re.sub(
        r'(<div class="p-6 flex justify-between items-center border-b border-hairline">\s*)'
        r'<div class="font-display-xl-mobile text-headline-lg font-bold text-on-surface">Taiwo Fadoyin</div>',
        r'\1<a href="index.html" class="font-display-xl-mobile text-headline-lg font-bold text-on-surface '
        r'hover:text-primary-fixed-dim transition-colors">Taiwo Fadoyin</a>',
        html,
        count=1,
    )
    return html


def hire_me_links(html: str) -> str:
    patterns = [
        (
            r'<button class="hidden md:block bg-primary-fixed-dim[^"]*">\s*Hire me\s*</button>',
            '<a href="contact.html" class="hidden md:block bg-primary-fixed-dim text-on-primary px-6 py-2.5 '
            'rounded font-bold hover:brightness-110 active:scale-95 transition-all">Hire me</a>',
        ),
        (
            r'<button class="bg-primary-container text-on-primary font-bold px-4 py-2 rounded[^"]*">'
            r"Hire me</button>",
            '<a href="contact.html" class="bg-primary-container text-on-primary font-bold px-4 py-2 '
            'rounded transition-transform active:scale-95 inline-block">Hire me</a>',
        ),
        (
            r'<button class="bg-primary-fixed text-on-primary-fixed font-bold px-4 py-2 rounded[^"]*">'
            r"Hire me</button>",
            '<a href="contact.html" class="bg-primary-fixed text-on-primary-fixed font-bold px-4 py-2 '
            'rounded transition-transform active:scale-95 inline-block">Hire me</a>',
        ),
        (
            r'<button class="bg-primary-fixed-dim text-on-primary font-bold px-4 py-2 rounded-lg[^"]*">'
            r"Hire me</button>",
            '<a href="contact.html" class="bg-primary-fixed-dim text-on-primary font-bold px-4 py-2 '
            'rounded-lg hover:scale-105 active:scale-95 transition-all inline-block">Hire me</a>',
        ),
        (
            r'<button class="w-full bg-primary-fixed-dim text-on-primary p-4 rounded-lg font-bold">'
            r"Hire me</button>",
            '<a href="contact.html" class="w-full bg-primary-fixed-dim text-on-primary p-4 rounded-lg '
            'font-bold text-center block">Hire me</a>',
        ),
        (
            r'<button class="w-full bg-primary-fixed text-on-primary-fixed font-bold py-4 rounded-lg">'
            r"Hire me</button>",
            '<a href="contact.html" class="w-full bg-primary-fixed text-on-primary-fixed font-bold py-4 '
            'rounded-lg text-center block">Hire me</a>',
        ),
        (
            r'<button class="w-full bg-primary-fixed-dim text-black font-bold py-4 rounded uppercase">'
            r"Hire me</button>",
            '<a href="contact.html" class="w-full bg-primary-fixed-dim text-black font-bold py-4 rounded '
            'uppercase text-center block">Hire me</a>',
        ),
        (
            r'<button class="mt-8 w-full bg-primary-fixed text-on-primary-fixed font-bold py-4 rounded-lg">'
            r"Hire me</button>",
            '<a href="contact.html" class="mt-8 w-full bg-primary-fixed text-on-primary-fixed font-bold py-4 '
            'rounded-lg text-center block">Hire me</a>',
        ),
    ]
    for pattern, replacement in patterns:
        html = re.sub(pattern, replacement, html, count=1)
    return html


def home_ctas(html: str) -> str:
    html = re.sub(
        r'<button class="bg-primary-fixed-dim text-on-primary px-8 py-4 rounded-lg font-bold flex items-center justify-center gap-2 hover:brightness-110 transition-all">\s*Hire me',
        '<a href="contact.html" class="bg-primary-fixed-dim text-on-primary px-8 py-4 rounded-lg font-bold flex items-center justify-center gap-2 hover:brightness-110 transition-all">\n                    Hire me',
        html,
        count=1,
    )
    html = re.sub(
        r'(Hire me <span class="font-label-mono">→</span>\s*)</button>',
        r"\1</a>",
        html,
        count=1,
    )
    html = re.sub(
        r'<button class="border border-hairline text-on-surface px-8 py-4 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-surface-variant transition-all">\s*View work\s*</button>',
        '<a href="work.html" class="border border-hairline text-on-surface px-8 py-4 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-surface-variant transition-all">\n                    View work\n                </a>',
        html,
        count=1,
    )
    return html


def about_ctas(html: str) -> str:
    html = re.sub(
        r'<button class="group flex items-center gap-3 bg-primary-fixed[^"]*"[^>]*>\s*'
        r'<span class="material-symbols-outlined">download</span>\s*'
        r"<span>Download CV</span>\s*</button>",
        '<a href="contact.html" class="group flex items-center gap-3 bg-primary-fixed '
        'text-on-primary-fixed font-bold px-8 py-4 rounded transition-all active:scale-95 '
        'hover:bg-primary-fixed-dim"><span class="material-symbols-outlined">download</span>'
        "<span>Download CV</span></a>",
        html,
        count=1,
    )
    html = re.sub(
        r'<button class="flex items-center gap-3 border border-hairline[^"]*"[^>]*>\s*'
        r"Get in touch\s*</button>",
        '<a href="contact.html" class="flex items-center gap-3 border border-hairline '
        "text-on-surface font-bold px-8 py-4 rounded transition-all hover:border-on-surface "
        'active:scale-95">Get in touch</a>',
        html,
        count=1,
    )
    return html


def set_active_nav(html: str, active: str) -> str:
    for label in NAV_LABELS:
        target = NAV_FILES[label]
        if label == active:
            html = re.sub(
                rf'(<a class=")[^"]*(" href="{re.escape(target)}">){re.escape(label)}',
                rf"\1{ACTIVE_CLASS}\2{label}",
                html,
            )
            html = re.sub(
                rf'(<a class=")font-body-md text-body-sm[^"]*(" href="{re.escape(target)}">)'
                rf"{re.escape(label)}",
                rf"\1{ACTIVE_CLASS}\2{label}",
                html,
            )
        else:
            html = re.sub(
                rf'(<a class=")[^"]*(" href="{re.escape(target)}">){re.escape(label)}',
                rf"\1{INACTIVE_CLASS}\2{label}",
                html,
            )
            html = re.sub(
                rf'(<a class=")font-body-md text-body-sm[^"]*(" href="{re.escape(target)}">)'
                rf"{re.escape(label)}",
                rf'\1font-body-md text-body-sm uppercase tracking-wider {INACTIVE_CLASS}\2{label}',
                html,
            )
    return html


def canonical_url(filename: str) -> str:
    if filename == "index.html":
        return f"{SITE_URL}/"
    return f"{SITE_URL}/{filename}"


def apply_contact_details(html: str) -> str:
    html = html.replace("hello@taiwofadoyin.com", EMAIL)
    html = html.replace("hello@jordan.dev", EMAIL)
    html = html.replace("hello@example.com", EMAIL)
    html = html.replace("'hello@example.com'", EMAIL)
    html = html.replace(f"placeholder=\"'{EMAIL}'\"", f'placeholder="{EMAIL}"')
    html = html.replace("Based in Lagos", "Based in United Kingdom")
    html = html.replace(
        'href="#">LinkedIn',
        f'href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn',
    )
    html = html.replace('href="#">Email', f'href="mailto:{EMAIL}">Email')
    html = html.replace('href="contact.html">Email', f'href="mailto:{EMAIL}">Email')
    return html


def apply_domain(html: str, filename: str) -> str:
    html = html.replace("jordan.dev", DOMAIN)
    html = html.replace("taiwofadoyin.com", DOMAIN)
    html = html.replace(f"http://{DOMAIN}", SITE_URL)
    html = html.replace(f"https://https://", "https://")  # guard double scheme

    title = PAGE_TITLES[filename]
    if re.search(r"<title>[^<]*</title>", html, re.IGNORECASE):
        html = re.sub(
            r"<title>[^<]*</title>",
            f"<title>{title}</title>",
            html,
            count=1,
            flags=re.IGNORECASE,
        )
    else:
        html = re.sub(r"(<head[^>]*>)", rf"\1\n<title>{title}</title>", html, count=1)

    canonical = canonical_url(filename)
    if 'rel="canonical"' not in html:
        meta = (
            f'<link rel="canonical" href="{canonical}">\n'
            f'<meta name="description" content="Taiwo Fadoyin — full-stack developer portfolio at {DOMAIN}">\n'
            f'<meta property="og:url" content="{canonical}">\n'
            f'<meta property="og:site_name" content="Taiwo Fadoyin">\n'
        )
        html = re.sub(r"(<head[^>]*>)", rf"\1\n{meta}", html, count=1)

    return html


def fix_portrait_url(html: str) -> str:
    return html.replace(PORTRAIT_PRIVATE, PORTRAIT_PUBLIC)


def image_filename_for_url(url: str) -> str:
    for key, name in IMAGE_URL_KEYS:
        if key in url:
            return name
    return f"asset-{hashlib.sha256(url.encode()).hexdigest()[:10]}.png"


def download_image(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return True
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; portfolio-build/1.0)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            dest.write_bytes(response.read())
        return dest.stat().st_size > 0
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        print(f"  warning: could not download {dest.name}: {err}")
        return False


def localize_images() -> None:
    images_dir = SITE / "images"
    images_dir.mkdir(exist_ok=True)

    url_to_local: dict[str, str] = {}
    for html_path in sorted(SITE.glob("*.html")):
        html = html_path.read_text(encoding="utf-8")
        for url in set(re.findall(r"https://lh3\.googleusercontent\.com/[^\s\"'<>]+", html)):
            if url in url_to_local:
                continue
            filename = image_filename_for_url(url)
            dest = images_dir / filename
            if download_image(url, dest):
                url_to_local[url] = f"images/{filename}"
            elif filename == "portrait.png" and LOCAL_PORTRAIT.exists():
                shutil.copy2(LOCAL_PORTRAIT, dest)
                url_to_local[url] = f"images/{filename}"

    for html_path in SITE.glob("*.html"):
        html = html_path.read_text(encoding="utf-8")
        for url, local in url_to_local.items():
            html = html.replace(url, local)
        html_path.write_text(html, encoding="utf-8")

    count = len(list(images_dir.glob("*")))
    print(f"  images: {count} file(s) in site/images/")


def process(filename: str, source: str, active: str) -> None:
    html = (ROOT / source).read_text(encoding="utf-8")
    html = fix_portrait_url(html)
    html = replace_nav_hrefs(html)
    html = fix_drawer_icon_links(html)
    html = brand_link(html)
    html = hire_me_links(html)
    html = apply_contact_details(html)
    html = apply_domain(html, filename)
    if filename == "index.html":
        html = home_ctas(html)
    if filename == "about.html":
        html = about_ctas(html)
    html = set_active_nav(html, active if active in NAV_LABELS else "Home")
    (SITE / filename).write_text(html, encoding="utf-8")


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    for out_name, source, active in PAGES:
        process(out_name, source, active)
    localize_images()
    (ROOT / "index.html").write_text(
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta http-equiv="refresh" content="0; url=site/index.html">\n'
        f'<title>Taiwo Fadoyin — {DOMAIN}</title>\n</head>\n<body>\n'
        f'<p><a href="site/index.html">Open portfolio</a> · '
        f'<a href="{SITE_URL}/">{DOMAIN}</a></p>\n</body>\n</html>\n',
        encoding="utf-8",
    )
    print(f"Built {len(PAGES)} pages in {SITE}")


if __name__ == "__main__":
    main()
