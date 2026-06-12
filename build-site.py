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
    "Home": ("home", "index.html"),
    "About": ("person", "about.html"),
    "Work": ("work", "work.html"),
    "Services": ("terminal", "services.html"),
    "Blog": ("article", "blog.html"),
}

NAV_LINK_BASE = "font-body-md text-body-md uppercase tracking-wider"
NAV_LINK_ACTIVE = (
    f"{NAV_LINK_BASE} text-primary-fixed-dim font-bold border-b "
    "border-primary-fixed-dim pb-1 transition-colors duration-200"
)
NAV_LINK_INACTIVE = (
    f"{NAV_LINK_BASE} text-on-surface-variant font-medium "
    "hover:text-primary-fixed-dim transition-colors duration-200"
)

NAV_SCRIPT = """<script id="site-nav-script">
    (function () {
        const mobileToggle = document.getElementById('mobile-menu-toggle');
        const sideNav = document.getElementById('side-nav');
        const sideNavClose = document.getElementById('side-nav-close');
        const sideNavOverlay = document.getElementById('side-nav-overlay');
        if (!mobileToggle || !sideNav) return;
        function toggleMenu() {
            sideNav.classList.toggle('translate-x-full');
            document.body.classList.toggle('overflow-hidden');
        }
        mobileToggle.addEventListener('click', toggleMenu);
        if (sideNavClose) sideNavClose.addEventListener('click', toggleMenu);
        if (sideNavOverlay) sideNavOverlay.addEventListener('click', toggleMenu);
    })();
</script>"""

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
CONTACT_FORM_PATH = "contact.html#contact-form"

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


def render_site_header(active: str) -> str:
    nav_links = "\n".join(
        f'<a class="{NAV_LINK_ACTIVE if label == active else NAV_LINK_INACTIVE}" '
        f'href="{href}">{label}</a>'
        for label, href in NAV_FILES.items()
    )
    drawer_links = "\n".join(
        (
            f'<a class="{"bg-primary-container text-on-primary-container rounded-lg p-4 flex items-center gap-4 font-label-mono text-label-mono transition-all" if label == active else "text-on-surface-variant p-4 flex items-center gap-4 font-label-mono text-label-mono hover:bg-surface-variant transition-all"}" '
            f'href="{href}">\n'
            f'<span class="material-symbols-outlined" data-icon="{icon}">{icon}</span> {label}\n'
            f"            </a>"
        )
        for label, (icon, href) in DRAWER_ICONS.items()
    )
    return f"""<!-- Site header (unified) -->
<nav class="docked full-width top-0 sticky z-50 bg-surface/80 dark:bg-surface/80 backdrop-blur-xl border-b border-hairline">
<div class="flex justify-between items-center w-full px-6 py-4 max-w-max-width mx-auto">
<a href="index.html" class="font-display-xl-mobile text-body-md font-bold text-on-surface flex items-center gap-2 after:content-[''] after:w-2 after:h-2 after:bg-primary-fixed-dim after:rounded-full after:animate-pulse hover:text-primary-fixed-dim transition-colors">Taiwo Fadoyin</a>
<div class="hidden md:flex items-center gap-8">
{nav_links}
</div>
<div class="flex items-center gap-4">
<button class="p-2 text-on-surface-variant hover:text-primary-fixed-dim transition-colors" type="button" aria-label="Toggle theme">
<span class="material-symbols-outlined" data-icon="dark_mode">dark_mode</span>
</button>
<a href="{CONTACT_FORM_PATH}" class="hidden md:block bg-primary-fixed-dim text-on-primary px-6 py-2.5 rounded font-bold hover:brightness-110 active:scale-95 transition-all">Hire me</a>
<button class="md:hidden text-on-surface" id="mobile-menu-toggle" type="button" aria-label="Open menu">
<span class="material-symbols-outlined" data-icon="menu">menu</span>
</button>
</div>
</div>
</nav>
<!-- Mobile drawer (unified) -->
<div class="fixed inset-0 z-[60] flex flex-col w-full md:hidden translate-x-full transition-transform duration-300" id="side-nav">
<div class="absolute inset-0 bg-black/50 backdrop-blur-sm" id="side-nav-overlay"></div>
<div class="relative ml-auto w-4/5 h-full bg-surface-container-highest flex flex-col border-l border-hairline shadow-2xl p-6">
<div class="flex justify-between items-center mb-12">
<a href="index.html" class="font-display-xl-mobile text-headline-lg font-bold text-on-surface hover:text-primary-fixed-dim transition-colors">Taiwo Fadoyin</a>
<button id="side-nav-close" type="button" aria-label="Close menu">
<span class="material-symbols-outlined" data-icon="close">close</span>
</button>
</div>
<div class="flex flex-col gap-2 flex-grow">
{drawer_links}
</div>
<div class="mt-auto pt-6 border-t border-hairline">
<p class="font-label-mono text-label-mono text-on-surface-variant mb-4">// Available for hire</p>
<a href="{CONTACT_FORM_PATH}" class="w-full bg-primary-fixed-dim text-on-primary p-4 rounded-lg font-bold text-center block">Hire me</a>
</div>
</div>
</div>"""


def strip_legacy_header(html: str) -> str:
    html = re.sub(
        r"<!-- Side Navigation \(Mobile Drawer\) -->.*?</aside>\s*",
        "",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"(<body[^>]*>).*?(<main\b)",
        r"\1\n\2",
        html,
        count=1,
        flags=re.DOTALL | re.IGNORECASE,
    )
    return html


def remove_legacy_nav_scripts(html: str) -> str:
    html = re.sub(
        r"<script>\s*function toggle(?:Menu|Nav|MobileNav)\(\)[\s\S]*?</script>\s*",
        "",
        html,
    )
    html = re.sub(
        r"\s*const mobileToggle = document\.getElementById\('mobile-menu-toggle'\);"
        r"[\s\S]*?sideNavOverlay\.addEventListener\('click', toggleMenu\);\s*",
        "\n",
        html,
    )
    html = re.sub(
        r"\s*const menuToggle = document\.getElementById\('menu-toggle'\);"
        r"[\s\S]*?menuToggle\.addEventListener\('click', toggleMenu\);\s*",
        "\n",
        html,
    )
    return html


def inject_unified_header(html: str, active: str) -> str:
    html = strip_legacy_header(html)
    header = render_site_header(active if active in NAV_LABELS else "Home")
    html = re.sub(
        r"(<body[^>]*>)",
        rf"\1\n{header}\n",
        html,
        count=1,
        flags=re.IGNORECASE,
    )
    html = remove_legacy_nav_scripts(html)
    if 'id="site-nav-script"' not in html:
        html = re.sub(r"</body>", NAV_SCRIPT + "\n</body>", html, count=1, flags=re.IGNORECASE)
    return html


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
    for _label, (icon, target) in DRAWER_ICONS.items():
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
    html = re.sub(
        r'<button([^>]*)>\s*Hire me(\s*<[^>]+>\s*)?</button>',
        rf'<a href="{CONTACT_FORM_PATH}"\1>Hire me\2</a>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    html = re.sub(
        r'<button([^>]*)>\s*Hire me\s*<span([^>]*)>\s*arrow_forward\s*</span>\s*</button>',
        rf'<a href="{CONTACT_FORM_PATH}"\1>Hire me <span\2>arrow_forward</span></a>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return html


def link_page_ctas(html: str) -> str:
    cta = CONTACT_FORM_PATH
    swaps = [
        (
            r'<button class="w-full border border-hairline hover:bg-white/5 py-4 font-label-mono text-label-mono transition-colors">BOOK AUDIT</button>',
            f'<a href="{cta}" class="w-full border border-hairline hover:bg-white/5 py-4 font-label-mono text-label-mono transition-colors text-center block">BOOK AUDIT</a>',
        ),
        (
            r'<button class="w-full bg-primary-fixed-dim text-on-primary font-bold py-5 font-label-mono text-label-mono tracking-widest transition-transform active:scale-95">START BUILD</button>',
            f'<a href="{cta}" class="w-full bg-primary-fixed-dim text-on-primary font-bold py-5 font-label-mono text-label-mono tracking-widest transition-transform active:scale-95 text-center block">START BUILD</a>',
        ),
        (
            r'<button class="w-full border border-hairline hover:bg-white/5 py-4 font-label-mono text-label-mono transition-colors">LET\'S TALK</button>',
            f'<a href="{cta}" class="w-full border border-hairline hover:bg-white/5 py-4 font-label-mono text-label-mono transition-colors text-center block">LET\'S TALK</a>',
        ),
        (
            r'<button class="bg-primary-fixed text-on-primary-fixed font-bold px-12 py-6 rounded-none text-headline-lg-mobile transition-transform active:scale-95 whitespace-nowrap">START A PROJECT →</button>',
            f'<a href="{cta}" class="bg-primary-fixed text-on-primary-fixed font-bold px-12 py-6 rounded-none text-headline-lg-mobile transition-transform active:scale-95 whitespace-nowrap inline-block">START A PROJECT →</a>',
        ),
        (
            r'<button class="bg-primary-container text-on-primary font-bold px-8 py-3 rounded hover:opacity-90 transition-opacity w-full">Subscribe to the Log</button>',
            f'<a href="{cta}" class="bg-primary-container text-on-primary font-bold px-8 py-3 rounded hover:opacity-90 transition-opacity w-full text-center block">Subscribe to the Log</a>',
        ),
    ]
    for pattern, replacement in swaps:
        html = re.sub(pattern, replacement, html, count=1)
    return html


def home_ctas(html: str) -> str:
    html = re.sub(
        r'<button class="bg-primary-fixed-dim text-on-primary px-8 py-4 rounded-lg font-bold flex items-center justify-center gap-2 hover:brightness-110 transition-all">\s*Hire me',
        f'<a href="{CONTACT_FORM_PATH}" class="bg-primary-fixed-dim text-on-primary px-8 py-4 rounded-lg font-bold flex items-center justify-center gap-2 hover:brightness-110 transition-all">\n                    Hire me',
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
        f'<a href="{CONTACT_FORM_PATH}" class="group flex items-center gap-3 bg-primary-fixed '
        'text-on-primary-fixed font-bold px-8 py-4 rounded transition-all active:scale-95 '
        'hover:bg-primary-fixed-dim"><span class="material-symbols-outlined">download</span>'
        "<span>Download CV</span></a>",
        html,
        count=1,
    )
    html = re.sub(
        r'<button class="flex items-center gap-3 border border-hairline[^"]*"[^>]*>\s*'
        r"Get in touch\s*</button>",
        f'<a href="{CONTACT_FORM_PATH}" class="flex items-center gap-3 border border-hairline '
        "text-on-surface font-bold px-8 py-4 rounded transition-all hover:border-on-surface "
        'active:scale-95">Get in touch</a>',
        html,
        count=1,
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


CONTACT_FORM_SCRIPT = """<script id="contact-form-script">
    function handleFormSubmit(e) {
        e.preventDefault();
        const form = document.getElementById('contact-form');
        const success = document.getElementById('success-state');
        const error = document.getElementById('error-state');
        const button = form.querySelector('button[type="submit"]');
        const originalContent = button.innerHTML;
        button.innerHTML = '<span class="material-symbols-outlined animate-spin text-xl">progress_activity</span> Sending...';
        button.disabled = true;
        if (error) {
            error.classList.add('hidden');
            error.classList.remove('flex');
        }

        const data = new FormData(form);
        fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(data).toString()
        })
        .then(function (res) {
            if (!res.ok) throw new Error('Submit failed');
            form.style.opacity = '0';
            success.classList.remove('pointer-events-none', 'opacity-0');
            success.classList.add('opacity-100');
        })
        .catch(function () {
            button.innerHTML = originalContent;
            button.disabled = false;
            if (error) {
                error.classList.remove('hidden');
                error.classList.add('flex');
            }
        });
    }

    function resetForm() {
        const form = document.getElementById('contact-form');
        const success = document.getElementById('success-state');
        const error = document.getElementById('error-state');
        const button = form.querySelector('button[type="submit"]');
        form.reset();
        form.style.opacity = '1';
        button.innerHTML = 'Send Transmission <span class="material-symbols-outlined">send</span>';
        button.disabled = false;
        success.classList.add('pointer-events-none', 'opacity-0');
        success.classList.remove('opacity-100');
        if (error) {
            error.classList.add('hidden');
            error.classList.remove('flex');
        }
    }

    if (window.location.hash === '#contact-form') {
        document.getElementById('contact-form')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
</script>"""


def wire_contact_form(html: str) -> str:
    html = re.sub(
        r'<script>\s*function toggleNav[\s\S]*?</script>\s*',
        "",
        html,
    )
    html = re.sub(
        r'<form class="space-y-8" id="contact-form" onsubmit="handleFormSubmit\(event\)">',
        (
            '<form class="space-y-8" id="contact-form" name="contact" method="POST" '
            'data-netlify="true" data-netlify-honeypot="bot-field" netlify '
            f'action="/{CONTACT_FORM_PATH.split("#")[0]}" '
            'onsubmit="handleFormSubmit(event)">\n'
            '<input type="hidden" name="form-name" value="contact" />\n'
            '<p class="hidden" aria-hidden="true"><label>Do not fill this out: '
            '<input name="bot-field" tabindex="-1" autocomplete="off" /></label></p>'
        ),
        html,
        count=1,
    )
    html = re.sub(
        r'(<label[^>]*>const sender_name =</label>\s*<input)([^>]*)(type="text")',
        r'\1 name="name"\2\3',
        html,
        count=1,
    )
    html = re.sub(
        r'(<label[^>]*>const sender_email =</label>\s*<input)([^>]*)(type="email")',
        r'\1 name="email"\2\3',
        html,
        count=1,
    )
    html = html.replace('name="type" type="radio"', 'name="project_type" type="radio"')
    html = re.sub(
        r'(<input checked="" class="hidden peer" name="project_type" type="radio")([^>]*)>'
        r'\s*<div[^>]*>WEB APP</div>',
        r'\1 value="Web app"\2>\n<div class="px-4 py-2 border border-hairline rounded-full text-center font-label-mono text-label-mono text-on-surface-variant peer-checked:bg-primary-fixed-dim peer-checked:border-primary-fixed-dim peer-checked:text-on-primary transition-all">WEB APP</div>',
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'(<input class="hidden peer" name="project_type" type="radio")([^>]*)>'
        r'\s*<div[^>]*>DESIGN</div>',
        r'\1 value="Design"\2>\n<div class="px-4 py-2 border border-hairline rounded-full text-center font-label-mono text-label-mono text-on-surface-variant peer-checked:bg-primary-fixed-dim peer-checked:border-primary-fixed-dim peer-checked:text-on-primary transition-all">DESIGN</div>',
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'(<input class="hidden peer" name="project_type" type="radio")([^>]*)>'
        r'\s*<div[^>]*>CONSULTING</div>',
        r'\1 value="Consulting"\2>\n<div class="px-4 py-2 border border-hairline rounded-full text-center font-label-mono text-label-mono text-on-surface-variant peer-checked:bg-primary-fixed-dim peer-checked:border-primary-fixed-dim peer-checked:text-on-primary transition-all">CONSULTING</div>',
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'(<label[^>]*>const message_body =</label>\s*<textarea)([^>]*)(rows=)',
        r'\1 name="message"\2\3',
        html,
        count=1,
    )
    if 'id="error-state"' not in html:
        html = html.replace(
            '<div class="absolute inset-0 bg-surface flex flex-col items-center justify-center p-12 text-center opacity-0 pointer-events-none transition-opacity duration-500" id="success-state">',
            (
                '<div class="hidden flex-col items-center justify-center p-8 mb-4 rounded-lg border border-error/40 bg-error/10 text-error" id="error-state">\n'
                '<p class="font-label-mono text-label-mono text-center">Transmission failed. Email <a class="underline" href="mailto:'
                + EMAIL
                + f'">{EMAIL}</a> directly.</p>\n</div>\n'
                '<div class="absolute inset-0 bg-surface flex flex-col items-center justify-center p-12 text-center opacity-0 pointer-events-none transition-opacity duration-500" id="success-state">'
            ),
        )
    if 'id="contact-form-script"' not in html:
        html = re.sub(
            r"</body>",
            CONTACT_FORM_SCRIPT + "\n</body>",
            html,
            count=1,
            flags=re.IGNORECASE,
        )
    return html


def write_netlify_forms_detection() -> None:
    (SITE / "forms.html").write_text(
        "<!DOCTYPE html>\n<html><head><title>Forms</title></head><body>\n"
        '<form name="contact" netlify netlify-honeypot="bot-field" hidden>\n'
        '  <input type="text" name="name" />\n'
        '  <input type="email" name="email" />\n'
        '  <input type="radio" name="project_type" value="Web app" />\n'
        '  <textarea name="message"></textarea>\n'
        "</form>\n</body></html>\n",
        encoding="utf-8",
    )


def process(filename: str, source: str, active: str) -> None:
    html = (ROOT / source).read_text(encoding="utf-8")
    html = fix_portrait_url(html)
    html = apply_contact_details(html)
    html = apply_domain(html, filename)
    if filename == "index.html":
        html = home_ctas(html)
    if filename == "about.html":
        html = about_ctas(html)
    html = hire_me_links(html)
    html = link_page_ctas(html)
    html = inject_unified_header(html, active)
    if filename == "contact.html":
        html = wire_contact_form(html)
    (SITE / filename).write_text(html, encoding="utf-8")


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    for out_name, source, active in PAGES:
        process(out_name, source, active)
    localize_images()
    write_netlify_forms_detection()
    (SITE / "CNAME").write_text(f"{DOMAIN}\n", encoding="utf-8")
    (SITE / ".nojekyll").touch()
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
