# -*- coding: utf-8 -*-
"""HTML component builders mirroring the Velora template, skinned for MYSense."""
import html as _h, re

def esc(s): return _h.escape(str(s), quote=True)

# ---------- icons ----------
ARROW_NE = '<svg viewBox="0 0 10 10" class="icon-arrow" aria-hidden="true"><path d="M2 8 8 2M3 2h5v5"/></svg>'
ARROW_R  = '<svg viewBox="0 0 16 16" class="icon-arrow" aria-hidden="true"><path d="M2 8h12M9 3l5 5-5 5"/></svg>'
ARROW_L  = '<svg viewBox="0 0 16 16" class="icon-arrow" aria-hidden="true"><path d="M14 8H2M7 3 2 8l5 5"/></svg>'
PLUS     = '<svg viewBox="0 0 16 16" class="icon-arrow" aria-hidden="true"><path d="M8 2v12M2 8h12"/></svg>'
CLOSE    = '<svg viewBox="0 0 16 16" class="icon-arrow" aria-hidden="true"><path d="M3 3l10 10M13 3 3 13"/></svg>'
CHEVRON  = '<svg viewBox="0 0 22 40" aria-hidden="true"><path d="M3 4l12 16L3 36" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PLAY     = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 2.5v9l8-4.5z" fill="currentColor"/></svg>'
STAR     = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5l2 4.3 4.7.5-3.5 3.2 1 4.6L8 11.8l-4.2 2.3 1-4.6L1.3 6.3 6 5.8z" fill="currentColor"/></svg>'
SOC = {
 'facebook':'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.3H7.4V14h2.8v8h3.3z"/></svg>',
 'instagram':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
 'linkedin':'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.5 8.5H3.3V21h3.2V8.5zM4.9 3a1.9 1.9 0 100 3.8 1.9 1.9 0 000-3.8zM21 13.3c0-3.4-1.8-5-4.3-5-2 0-2.9 1.1-3.4 1.9V8.5h-3.2V21h3.2v-6.9c0-1.8.3-3.6 2.6-3.6 2.2 0 2.2 2.1 2.2 3.7V21H21v-7.7z"/></svg>',
 'youtube':'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.6 7.2a2.5 2.5 0 00-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 002.4 7.2 26 26 0 002 12a26 26 0 00.4 4.8 2.5 2.5 0 001.8 1.8c1.6.4 7.8.4 7.8.4s6.2 0 7.8-.4a2.5 2.5 0 001.8-1.8A26 26 0 0022 12a26 26 0 00-.4-4.8zM10 15V9l5.2 3L10 15z"/></svg>',
 'tiktok':'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.5 3c.3 2.3 1.6 3.7 3.9 3.9v3.2c-1.5.1-2.8-.3-3.9-1.1v6.3a5.8 5.8 0 11-5-5.7v3.3a2.6 2.6 0 101.8 2.5V3h3.2z"/></svg>',
}

SITE = {
 'name':'MYSense','phone':'+6019-3541688','phone_href':'https://wa.me/60193541688','email':'contact@mysense.com.my',
 'address':'Level 2, Unit 011, 129 Offices Block J, Jaya One, Jalan Prof Diraja Ungku Aziz, 46200 Petaling Jaya, Selangor',
 'reg':'MYSENSE SDN BHD (1370034-P)',
 'socials':[('facebook','https://www.facebook.com/mysensemarketing'),('instagram','https://www.instagram.com/mysense.com.my/'),('linkedin','https://www.linkedin.com/company/mysense-marketing/'),('youtube','https://www.youtube.com/@mysensemarketing1036'),('tiktok','https://www.tiktok.com/@mysense.im')],
}

def roll(text, cls=''):
    t=esc(text)
    return f'<span class="roll {cls}"><span class="roll__in"><span>{t}</span><span>{t}</span></span></span>'

def label(text, light=False):
    return f'<span class="label{" label--light" if light else ""}">{esc(text)}</span>'

def btn(text, href='#', light=False, extra='', nav=False, full=False):
    cls='btn'+(' btn--light' if light else '')+(' btn--nav' if nav else '')+(' btn--full' if full else '')+(' '+extra if extra else '')
    r = roll(text,'roll--sm') if nav else roll(text)
    return f'<a class="{cls}" href="{esc(href)}"><span class="btn__label">{r}</span><span class="btn__icon">{ARROW_NE}</span></a>'

def alink(text, href='#'):
    return f'<a class="alink rollhost" href="{esc(href)}">{roll(text)}{ARROW_R}</a>'

def sq(href=None, small=False, title='Open'):
    inner=f'<span class="sq{" sq--sm" if small else ""}">{ARROW_NE}</span>'
    return f'<a href="{esc(href)}" aria-label="{esc(title)}">{inner}</a>' if href else inner

def avatars(imgs, size=None):
    return '<span class="avatars">'+''.join(f'<img src="{esc(i)}" alt="" loading="lazy">' for i in imgs)+'</span>'

def trust(imgs, score='4.9/5', sub='Trusted by', strong='300+ brands in Malaysia'):
    return (f'<div class="trust">{avatars(imgs)}<div class="trust__txt"><span class="trust__score">{esc(score)}</span>'
            f'<span class="trust__sub">{esc(sub)} <b>{esc(strong)}</b></span></div></div>')

# ---------- header / menu / footer ----------
CARET='<svg viewBox="0 0 10 10" class="icon-arrow" aria-hidden="true"><path d="M2 3.5 5 6.5l3-3"/></svg>'
SERVICES_MENU=[('Search Engine Optimisation','/services/seo/'),('Generative Engine Optimisation','/services/geo/'),('Search Engine Marketing','/services/sem/'),('Social Media Marketing','/services/social-media-marketing/'),('Web Development','/services/web-development/'),('Web Analytic Services','/services/web-analytics/'),('Influencer Marketing','/services/influencer-marketing/'),('Xiaohongshu Marketing','/services/xiaohongshu-marketing/'),('TikTok Marketing','/services/tiktok-marketing/'),('Business Consultancy','/services/business-consultancy/'),('White Label','/white-label/')]
INDUSTRIES_MENU=[('Medical Marketing','/industries/medical-marketing/'),('Automotive','/industries/automotive/'),('Finance','/industries/finance/'),('Beauty & Wellness','/industries/beauty-wellness/'),('Home Improvement','/industries/home-improvement/'),('Education','/industries/education/'),('F&B','/industries/food-beverage/'),('B2B','/industries/b2b/'),('Fashion Brand','/industries/fashion/')]
WORKS_MENU=[('Google SEO Case Studies','/case-studies/#seo'),('Social Media Case Studies','/case-studies/#social'),('Influencer Marketing Case Studies','/case-studies/#influencer'),('Google Ads Case Studies','/case-studies/#ads'),('Website Development Case Studies','/services/web-development/#showcase')]
NAV=[('Services','/services/',SERVICES_MENU),('We Work With','/industries/',INDUSTRIES_MENU),('About Us','/about/',None),('Blog','/insights/',None),('Event','/event/',None),('Our Works','/case-studies/',WORKS_MENU),('Career','/career/',None),('Creator','/creator/',None)]

def _dd(items, root, cols=2):
    lis=''.join(f'<a href="{root}{h.lstrip("/")}" class="rollhost">{roll(t)}</a>' for t,h in items)
    return f'<div class="dd" style="--cols:{cols}"><div class="dd__in">{lis}</div></div>'

def header(root):
    links=''
    for t,h,sub in NAV:
        if sub:
            links+=f'<div class="nav__item has-dd"><a class="nav__link rollhost" href="{root}{h.lstrip("/")}" aria-haspopup="true">{roll(t)}<span class="caret">{CARET}</span></a>{_dd(sub,root,2 if len(sub)>6 else 1)}</div>'
        else:
            links+=f'<div class="nav__item"><a class="nav__link rollhost" href="{root}{h.lstrip("/")}">{roll(t)}</a></div>'
    menu=''
    for t,h,sub in NAV+[('Contact Us','/contact/',None)]:
        menu+=f'<a href="{root}{h.lstrip("/")}">{roll(t)}</a>'
        if sub: menu+='<div class="menu__sub">'+''.join(f'<a href="{root}{x.lstrip("/")}">{esc(n)}</a>' for n,x in sub)+'</div>'
    return f'''<header class="header"><nav class="nav" aria-label="Main">
  <a class="nav__logo" href="{root}" aria-label="MYSense home"><img src="{root}assets/img/brand/logo_white_mark.png" alt="MYSense" width="227" height="34"></a>
  <div class="nav__links">{links}</div>
  {btn('Contact Us', root+'contact/', light=True, nav=True)}
  <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span></button>
</nav></header>
<div class="menu" aria-hidden="true">
  <div class="menu__top"><a href="{root}"><img src="{root}assets/img/brand/logo_white_mark.png" alt="MYSense"></a><button class="menu__close" aria-label="Close menu">{CLOSE}</button></div>
  <div class="menu__body">
    <div class="menu__links">{menu}</div>
    <div class="menu__side">
      <img class="menu__img" src="{root}assets/img/about-team.jpg" alt="The MYSense team at Jaya One, Petaling Jaya" loading="lazy">
      <div class="menu__meta">
        <div class="socials">{''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{SOC[n]}</a>' for n,u in SITE["socials"][:3])}</div>
        <div class="menu__contact"><span class="t-small">Contact</span><a class="rollhost" href="mailto:{SITE["email"]}">{roll(SITE["email"])}</a><a class="rollhost" href="{SITE["phone_href"]}">{roll(SITE["phone"])}</a></div>
      </div>
    </div>
  </div>
</div>'''

def footer(root):
    quick=[('Home','/'),('Case Studies','/case-studies/','5'),('About Us','/about/'),('Services','/services/'),('Insights','/insights/'),('Career','/career/')]
    svc=[('Search Engine Optimisation','/services/seo/'),('Generative Engine Optimisation','/services/geo/'),('Search Engine Marketing','/services/sem/'),('Social Media Marketing','/services/social-media-marketing/'),('Influencer Marketing','/services/influencer-marketing/'),('Website Development','/services/web-development/')]
    loc=[('SEO Kuala Lumpur','/seo-kuala-lumpur/'),('SEO Johor Bahru','/seo-johor-bahru/'),('SEO Penang','/seo-penang/'),('SEO Selangor','/seo-selangor/')]
    def col(title, items):
        lis=''.join(f'<li><a class="rollhost" href="{root}{h.lstrip("/")}">{roll(t)}{("<span class=badge>"+x[2]+"</span>") if len(x)>2 else ""}</a></li>' for x in items for t,h in [x[:2]])
        return f'<div class="fcol"><h5>{esc(title)}</h5><ul>{lis}</ul></div>'
    contact=f'''<div class="fcol"><h5>Contact</h5><ul><li><a class="rollhost" href="mailto:{SITE["email"]}">{roll(SITE["email"])}</a></li><li><a class="rollhost" href="{SITE["phone_href"]}">{roll(SITE["phone"])}</a></li><li><span style="color:var(--g-600);display:block;max-width:220px">{esc(SITE["address"])}</span></li></ul></div>'''
    socials=''
    contact=contact.replace('</ul></div>','</ul><div class="socials" style="margin-top:14px">'+''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{SOC[n]}</a>' for n,u in SITE["socials"])+'</div></div>')
    return f'''<footer class="footer">
  <div class="wrap footer__in">
    <div class="footer__brand">
      <a href="{root}"><img class="logo" src="{root}assets/img/brand/logo_black_mark.png" alt="MYSense"></a>
      <div class="news"><p class="t-19">Join Our <span>Newsletter</span></p>
        <form class="news__form" data-mock><input type="email" placeholder="name@company.com" aria-label="Email"><button type="submit">Submit</button></form>
        <p class="t-small">No spam. Just digital marketing insights for Malaysian brands.</p></div>
    </div>
    <div class="footer__cols">{col('Quick Links',quick)}{col('Services',svc)}{col('Location',loc)}{contact}{socials}</div>
  </div>
  <div class="footer__bar"><div class="wrap">
    <span class="copy">© <span data-year>2026</span> {esc(SITE["reg"])}. All rights reserved.</span>
    <span class="legal"><a class="rollhost" href="{root}privacy-policy/">{roll('Privacy Policy','roll--sm')}</a><a class="rollhost" href="{root}terms-of-services/">{roll('Terms of Service','roll--sm')}</a><a class="rollhost" href="{root}job-scam/">{roll('Job Scam Alert','roll--sm')}</a></span>
    <span class="made">Head office <a class="rollhost" href="https://maps.google.com/?cid=4982863949701831771" target="_blank" rel="noopener">{roll('Jaya One, Petaling Jaya')}</a></span>
  </div></div>
</footer>'''

# ---------- section builders ----------
def section(inner, cls='section', id=None, wrap=True, rv=True):
    i=f' id="{id}"' if id else ''
    inner = f'<div class="wrap">{inner}</div>' if wrap else inner
    return f'<section class="{cls}"{i}>{inner}</section>'

def head_split(lbl, title, sub=None, display=True, rv=True):
    t='t-display' if display else 't-h1'
    return (f'<div class="head-split"><div class="rv">{label(lbl)}</div><div class="head-split__right">'
            f'<h2 class="{t} rv">{title}</h2>'+(f'<p class="t-19 rv">{sub}</p>' if sub else '')+'</div></div>')

def head_stack(lbl, title, sub=None, light=False, cls='t-h2', maxw=None):
    st=f' style="max-width:{maxw}px"' if maxw else ''
    return (f'<div class="head-stack"{st}><div class="rv">{label(lbl,light)}</div><h2 class="{cls} rv">{title}</h2>'+(f'<p class="t-body muted rv">{sub}</p>' if sub else '')+'</div>')

def case_card(c, root):
    stats=''.join(f'<div class="stat-box"><span class="stat-box__v">{esc(s[0])}</span><span class="stat-box__l">{esc(s[1])}</span></div>' for s in c['stats'][:2])
    logo=f'<img class="case-card__logo" src="{root}{c["logo"]}" alt="{esc(c["client"])} logo" loading="lazy">' if c.get('logo') else f'<span class="t-19">{esc(c["client"])}</span>'
    overlay=f'<img class="overlay-logo" src="{root}{c["logo"]}" alt="" loading="lazy">' if c.get('logo') else ''
    return f'''<a class="case-card rv" href="{root}{c['href'].lstrip('/')}">
  <div class="case-card__media"><img class="cover" src="{root}{c['image']}" alt="{esc(c['alt'])}" loading="lazy">{overlay}<span class="grain"></span></div>
  {logo}
  <p class="case-card__desc">{esc(c['desc'])}</p>
  <div class="case-card__stats">{stats}<span class="sq">{ARROW_NE}</span></div>
</a>'''

def logo_grid(logos, root):
    return '<div class="logo-grid" data-stagger="0.06">'+''.join(f'<div class="logo-card rv"><img src="{root}assets/img/logos/{f}" alt="{esc(n)}" loading="lazy"></div>' for n,f in logos)+'</div>'

def clients_strip(root, logos, est='300+ brands'):
    return f'''<div class="clients__row rv"><span class="label">Selected Clients &amp; Partners</span><span class="plus">{PLUS}</span><span class="est">{esc(est)}</span><span class="plus plus--2">{PLUS}</span><span class="ghost"></span></div>{logo_grid(logos, root)}'''

def stat_card(v, suf, lbl, desc=None, pre='', short=False):
    d=f'<p class="stat-card__d">{esc(desc)}</p>' if desc else ''
    return f'<div class="stat-card{" stat-card--short" if short else ""} rv"><div class="stat-card__v">{("<em>"+esc(pre)+"</em>") if pre else ""}{esc(v)}<em>{esc(suf)}</em></div><div class="stat-card__l">{esc(lbl)}</div>{d}</div>'

def steps(items):
    rows=''.join(f'<div class="step rv"><span class="step__n t-num">{i+1:02d}</span><div class="step__body"><h3 class="t-24">{esc(t)}</h3><p>{esc(d)}</p></div></div>' for i,(t,d) in enumerate(items))
    return f'<div class="process__steps" data-stagger="0.08">{rows}</div>'

def accordion(items, root):
    out=[]
    for i,it in enumerate(items):
        lst=''.join(f'<li>{PLUS}<span>{esc(x)}</span></li>' for x in it.get('list',[]))
        img=f'<img class="acc__media" src="{root}{it["image"]}" alt="{esc(it.get("alt",""))}" loading="lazy">' if it.get('image') else ''
        more=f'<p class="acc__desc">{esc(it["desc"])}</p>' + (f'<p style="margin-top:24px">{alink("Learn more", root+it["href"].lstrip("/"))}</p>' if it.get('href') else '')
        out.append(f'''<div class="acc__item rv"><span class="acc__num">{i+1:02d}</span>
  <button class="acc__title" aria-expanded="false"><h4 class="t-h4">{esc(it['title'])}</h4><span class="acc__toggle">{PLUS}</span></button>
  <div class="acc__listwrap"><div><ul class="acc__list">{lst}</ul></div></div>
  <div class="acc__content"><div>{img}{more}</div></div>
</div>''')
    return '<div class="acc">'+''.join(out)+'</div>'

def faq(items, root=None, help_block=None):
    rows=''.join(f'<div class="faq__item rv"><button class="faq__q" aria-expanded="false"><span>{esc(q)}</span><span class="faq__ic">{PLUS}</span></button><div class="faq__a"><div><p>{a}</p></div></div></div>' for q,a in items)
    return f'<div class="faq__list" data-stagger="0.06">{rows}</div>'

def tcard(t, root):
    cl = f'<img class="cl" src="{root}{t["logo"]}" alt="" loading="lazy">' if t.get('logo') else f'<span class="cl-txt">{esc(t.get("company",""))}</span>'
    av = f'<img class="av" src="{root}{t["avatar"]}" alt="" loading="lazy">' if t.get('avatar') else f'<span class="av" style="width:56px;height:56px;border-radius:999px;background:var(--dark);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600">{esc(t["name"][0])}</span>'
    return f'<div class="tcard"><div class="tcard__top">{av}{cl}</div><p class="tcard__q">{esc(t["quote"])}</p><p class="tcard__n">{esc(t["name"])}</p><p class="tcard__r">{esc(t.get("role",""))}</p></div>'

def post_big(p, root):
    return f'''<a class="post-big rv" href="{root}{p['href'].lstrip('/')}"><div class="post-big__img"><img src="{root}{p['image']}" alt="" loading="lazy"></div>
<div class="post-big__cap"><div><p class="t-small d">{esc(p['date'])}</p><p class="t">{esc(p['title'])}</p></div>{sq(small=True)}</div></a>'''

def post_sm(p, root):
    return f'''<a class="post-sm rv" href="{root}{p['href'].lstrip('/')}"><div class="post-sm__img"><img src="{root}{p['image']}" alt="" loading="lazy"></div>
<div class="post-sm__body"><p class="t">{esc(p['title'])}</p><div class="post-sm__foot"><span class="t-small d">{esc(p['date'])}</span>{sq(small=True)}</div></div></a>'''

def contact_band(root, bg, title='Talk To Us', text=None, direct='Prefer a direct conversation?', direct_btn=('Let’s Talk Now!','https://wa.me/60193541688')):
    text = text or "Tell us a bit about your business and we'll get back to you within 1-2 working days with the next steps."
    return f'''<section class="contact" id="general-form"><div class="contact__bg"><img src="{root}{bg}" alt="" loading="lazy"></div>
<div class="wrap contact__in">
  <form class="form-card rv" data-mock>
    <img class="logo" src="{root}assets/img/brand/logo_white_mark.png" alt="MYSense">
    <div class="field"><label for="f-name">Name</label><input id="f-name" type="text" placeholder="Your name" required></div>
    <div class="field"><label for="f-email">Company email</label><input id="f-email" type="email" placeholder="you@company.com" required></div>
    <div class="field"><label for="f-phone">WhatsApp number</label><input id="f-phone" type="tel" placeholder="+60"></div>
    <div class="field"><label for="f-msg">Tell us about your business</label><textarea id="f-msg" placeholder="Which services are you interested in, and what are your goals?"></textarea></div>
    <button class="btn btn--submit" type="submit">Get Your Free Strategy Plan</button>
    <p class="note">By submitting, you agree to our <a class="rollhost" href="{root}terms-of-services/">{roll('Terms')}</a> and <a class="rollhost" href="{root}privacy-policy/">{roll('Privacy Policy')}</a>.</p>
  </form>
  <div class="contact__txt"><h2 class="t-display rv">{title}</h2><p class="rv">{esc(text)}</p>
    <div class="contact__direct rv"><p class="t-24">{esc(direct)}</p>{btn(direct_btn[0], direct_btn[1] if direct_btn[1].startswith('http') else root+direct_btn[1].lstrip('/'), light=True)}</div></div>
</div></section>'''

def cta_panel(title, text, btn_text, href, root):
    return f'<section class="section section--tight"><div class="wrap"><div class="cta-panel rv"><div><h2 class="t-display">{title}</h2><p>{esc(text)}</p></div>{btn(btn_text, root+href.lstrip("/"), light=True)}</div></div></section>'

def page(title, desc, body, root, canonical=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="{root}assets/img/brand/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/main.css">
</head>
<body>
{header(root)}
<main>
{body}
</main>
{footer(root)}
<script src="{root}assets/js/main.js" defer></script>
</body>
</html>'''
