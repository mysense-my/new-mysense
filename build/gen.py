# -*- coding: utf-8 -*-
"""Generate the MYSense revamp (Velora layout) into ../site. Run: python3 gen.py"""
import os, re, shutil, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from components import *
import components as C

HERE=os.path.dirname(os.path.abspath(__file__)); ROOTDIR=os.path.abspath(os.path.join(HERE,'..'))
SITE=os.path.join(ROOTDIR,'site'); PAGES_MD=os.path.join(ROOTDIR,'00-current-site','pages')
AV=['assets/img/logos/giant.png','assets/img/logos/yamaha.png','assets/img/logos/eu-yan-sang.png']

def rel(path):
    depth=len([p for p in path.strip('/').split('/') if p]); return '../'*depth if depth else './'

def write(path, title, desc, body):
    root=rel(path); out=os.path.join(SITE, path.strip('/'), 'index.html') if path.strip('/') else os.path.join(SITE,'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out,'w',encoding='utf-8').write(page(title, desc, body(root), root))
    print('wrote', path)

# ---------- markdown (captured pages) → prose html ----------
def md_prose(slug, skip_h1=True, drop_until=None, stop_at=None, keep_buttons=False):
    p=os.path.join(PAGES_MD, slug+'.md'); s=open(p,encoding='utf-8').read()
    body=s.split('## Page content (document order)',1)[1]
    body=re.split(r'\n## (Other background|Images on this page|Embeds)',body)[0]
    out=[]; ul=[]; started=drop_until is None
    def flush():
        nonlocal ul
        if ul: out.append('<ul>'+''.join(f'<li>{esc(x)}</li>' for x in ul)+'</ul>'); ul=[]
    for ln in body.split('\n'):
        t=ln.strip()
        if not t: continue
        if not started:
            if drop_until in t: started=True
            continue
        if stop_at and stop_at in t: break
        if t.startswith(('[IMG]','[BG]','[CSS-BG]','===','<','→','[IFRAME]','[VIDEO','[COUNTER]','[INPUT','[LABEL','[TEXTAREA')): continue
        if t.startswith('[BTN]'):
            if keep_buttons: flush(); out.append(f'<p><strong>{esc(t[5:].strip())}</strong></p>')
            continue
        m=re.match(r'^(#+)\s*(.*)',t)
        if m:
            lvl=len(m.group(1)); txt=m.group(2)
            if lvl==1 and skip_h1: continue
            flush(); out.append(f'<h{min(lvl+1,4)}>{esc(txt)}</h{min(lvl+1,4)}>' if lvl>1 else f'<h2>{esc(txt)}</h2>')
        elif t.startswith('- '): ul.append(t[2:])
        elif re.match(r'^[●○]\s*',t): ul.append(re.sub(r'^[●○]\s*','',t))
        else: flush(); out.append(f'<p>{esc(t)}</p>')
    flush(); return '\n'.join(out)

# ---------- shared data ----------
LOGOS_ALL=[('Giant','giant.png'),('Klinik Suzana','klinik-suzana.png'),('Yamaha','yamaha.png'),('Eu Yan Sang','eu-yan-sang.png'),('Mamee','mamee.png'),('Subang Jaya Medical Centre','subang-jaya-medical-centre.png'),('FamilyMart','familymart.png'),('OldTown White Coffee','oldtown-white-coffee.png'),('Brother','brother.png'),('SENA Healthcare Services','sena-healthcare.png'),('MATTA Fair','matta-fair.png'),('Taiwan Expo','taiwan-expo.png'),
 ('ASEC','asec.png'),('Baagus','baagus.png'),('Dr Clear Aligners','dr-clear-aligners.png'),('Souper Tang','souper-tang.png'),('Senarco','senarco.png'),('Mummys Market','mummys-market.png'),('Arisun','arisun.png'),('First City University College','first-city-university-college.png'),('Pureen','pureen.png'),('Skin Renew','skin-renew.png'),('A Klinik','a-klinik.png'),('Dr Chong Clinic','dr-chong-clinic.png')]
LOGOS_HOME=LOGOS_ALL
LOGOS_ABOUT=LOGOS_ALL

CASES=[
 dict(slug='klinik-suzana-seo',client='Klinik Suzana',cat='Search Engine Optimisation',industry='Healthcare & aesthetics',logo='assets/img/logos/klinik-suzana.png',image='assets/img/cases/klinik-suzana.jpg',alt='Klinik Suzana team',
      desc='A long-term SEO strategy focusing on keyword expansion, content optimisation and technical improvements.',
      title='5,000+ Keywords Ranked with 250,000% Growth in Visibility',
      challenge='Klinik Suzana faced limited online visibility in a competitive aesthetic and healthcare market, with low search rankings and inconsistent traffic, restricting patient acquisition from digital channels.',
      strategy='MYSense implemented a long-term SEO strategy focusing on keyword expansion, content optimisation, and technical improvements to steadily increase search visibility and rankings.',
      stats=[('5,000+','Keywords Ranked'),('792','Keywords in Top 10'),('250,000%','Keywords Growth')],gallery=['assets/img/cases/seo-1.webp','assets/img/cases/seo-2.webp','assets/img/misc/strategic-1.webp']),
 dict(slug='baagus-seo',client='Baagus',cat='Search Engine Optimisation',industry='Home living',logo='assets/img/logos/baagus.png',image='assets/img/cases/baagus.jpg',alt='Baagus motorised curtains',
      desc='A structured SEO strategy focused on high-intent keyword expansion, content optimisation and technical improvements.',
      title='86% Growth in Organic Traffic with 650+ Keywords Ranked',
      challenge='Baagus, a home living brand, faced limited organic visibility and inconsistent search performance. Despite having a strong product offering, their website struggled to attract sustained traffic and rank competitively for relevant keywords in the home living space.',
      strategy='MYSense implemented a structured SEO strategy focused on high-intent keyword expansion, content optimization, and technical improvements to drive sustainable rankings. Continuous tracking and optimization ensured consistent growth in visibility and long-term organic performance.',
      stats=[('+86%','Organic Click Growth'),('650+','Ranking keywords')],gallery=['assets/img/cases/seo-2.webp','assets/img/cases/seo-1.webp','assets/img/misc/strategic-2.webp']),
 dict(slug='mmw-bone-alignment-seo',client='MMW Bone Alignment',cat='Search Engine Optimisation',industry='Healthcare (chiropractic)',logo=None,image='assets/img/cases/mmw.jpg',alt='MMW Bone Alignment',
      desc='A targeted SEO strategy focusing on high-intent medical keywords, content optimisation and local search.',
      title='500+ Keywords Ranked & 3,000% Traffic Growth in a Competitive Healthcare Niche',
      challenge='The client operated in a highly competitive healthcare niche (chiropractic & bone alignment), with low initial search visibility and minimal keyword rankings. Most high-intent keywords such as “slip disc treatment” and “chiropractor near me” were either not ranking or buried deep in search results.',
      strategy='MYSense implemented a targeted SEO strategy focusing on high-intent medical keywords, content optimization, and local search to build strong authority in the healthcare space.',
      stats=[('+3,295%','Organic Traffic Growth'),('550+','Ranking keywords'),('575,000+','Search Impressions Achieved')],gallery=['assets/img/cases/seo-1.webp','assets/img/misc/strategic-3.webp','assets/img/cases/seo-2.webp']),
 dict(slug='klinik-suzana-google-ads',client='Klinik Suzana',cat='Search Engine Marketing',industry='Healthcare & aesthetics',logo='assets/img/logos/klinik-suzana.png',image='assets/img/cases/klinik-suzana-ads.webp',alt='Klinik Suzana Google Ads',
      desc='Campaigns restructured, keyword targeting refined and ad copy optimised to comply with medical ad policies.',
      title='A Data-Driven Strategy That Delivered 80,000+ Conversions',
      challenge='The client encountered difficulties managing their Google Ads campaigns while promoting medical-related services. Strict advertising policies and keyword restrictions made it challenging to maintain stable campaign performance while reaching the right audience.',
      strategy='MYSense restructured campaigns, refined keyword targeting, and optimised ad copy to comply with policies while improving visibility and cost efficiency.',
      stats=[('37,000+','Clicks Generated'),('80,000+','Conversions'),('RM0.60','Cost Per Click')],gallery=['assets/img/cases/sem-1.webp','assets/img/cases/sem-2.webp','assets/img/cases/sem-3.webp']),
 dict(slug='baagus-google-ads',client='Baagus',cat='Search Engine Marketing',industry='Home living',logo='assets/img/logos/baagus.png',image='assets/img/cases/baagus.jpg',alt='Baagus Google Ads',
      desc='Campaign structure, keyword targeting and ad copy optimised with smarter bidding to improve relevance and reduce costs.',
      title='Driving Higher Traffic and Engagement at a Lower Cost',
      challenge='Baagus, a home living brand, faced limited visibility and inconsistent performance from paid search. Despite a strong product offering, campaigns struggled to attract sustained, relevant traffic at an efficient cost.',
      strategy='MYSense optimised campaign structure, keyword targeting, and ad copy while implementing smarter bidding to improve relevance and reduce costs.',
      stats=[('+48.7%','Click Increased'),('23.9%','Click Through Rate'),('RM0.91','Cost Per Conversion')],gallery=['assets/img/cases/sem-2.webp','assets/img/cases/sem-3.webp','assets/img/cases/sem-1.webp']),
 dict(slug='dental-clinic-google-ads',client='Dental Clinic',cat='Search Engine Marketing',industry='Dental',logo=None,image='assets/img/cases/dental-ads.webp',alt='Dental clinic Google Ads results',
      desc='Campaigns restructured and keyword targeting refined to lift conversions and cut cost per lead within a month.',
      title='178% Increase in Conversions within 1 Month',
      challenge='The dental clinic faced low conversion volume and high cost per lead, limiting campaign performance and making it difficult to scale profitably.',
      strategy='MYSense restructured campaigns, refined keyword targeting, and optimised ad copy to comply with policies while improving visibility and cost efficiency.',
      stats=[('+178%','Conversions Increased'),('-45%','Cost Per Conversion'),('-13%','Avg. Cost Per Click')],gallery=['assets/img/cases/sem-3.webp','assets/img/cases/sem-1.webp','assets/img/cases/sem-2.webp']),
 dict(slug='matta-fair-influencer-marketing',client='MATTA Fair',cat='Influencer Marketing',industry='Travel exhibition',logo='assets/img/logos/matta-fair.png',image='assets/img/cases/matta-fair.webp',alt='MATTA Fair influencer campaign',
      desc='Lifestyle and travel influencers created authentic, real-time Instagram Reels from one of Malaysia’s largest travel exhibitions.',
      title='41 Influencer Reels and 1.5M+ Reach for MATTA Fair',
      challenge='MATTA Fair aimed to increase digital awareness and social engagement for one of Malaysia’s largest travel exhibitions, while attracting more visitors and generating buzz across social media platforms.',
      strategy='MYSense executed a targeted Influencer Marketing campaign, collaborating with carefully selected lifestyle and travel influencers to create authentic, real-time content from the event. Influencers captured their experiences through engaging Instagram Reels, showcasing travel deals, event highlights, and on-ground activities to their audiences.',
      stats=[('41','Influencer Reels published'),('1.5M+','Total Reach'),('1.5M+','Total Impressions'),('34K+','Total Engagements')],gallery=['assets/img/cases/im-1.webp','assets/img/cases/im-2.webp','assets/img/cases/im-3.webp']),
 dict(slug='la-estephe-influencer-marketing',client='La Estephe',cat='Influencer Marketing',industry='Skincare',logo=None,image='assets/img/cases/la-estephe.webp',alt='La Estephe influencer campaign',
      desc='Influencer-led content across social media positioning the brand as a premium skincare choice.',
      title='60 Influencer Reels and 1.3M+ Impressions for La Estephe',
      challenge='Drive large-scale awareness and engagement for La Estephe through influencer-led content across social media, positioning the brand as a premium skincare choice.',
      strategy='MYSense matched La Estephe with lifestyle and beauty creators who produced Reels around the products, with content approval, usage rights and reporting handled end to end.',
      stats=[('60','Influencer Reels published'),('1.3M+','Total Impressions'),('39K+','Total Engagements')],gallery=['assets/img/cases/im-2.webp','assets/img/cases/im-3.webp','assets/img/cases/im-1.webp']),
 dict(slug='homedec-xiaohongshu',client='HOMEDEC',cat='Xiaohongshu Marketing',industry='Home & interior exhibition',logo=None,image='assets/img/cases/homedec.webp',alt='HOMEDEC Xiaohongshu campaign',
      desc='Niche home and lifestyle KOLs created platform-native XHS content for a design-conscious, Chinese-speaking audience.',
      title='Targeted XHS Awareness for HOMEDEC',
      challenge='Drive targeted awareness and engagement for HOMEDEC on XiaoHongShu (XHS) by leveraging relevant influencers to reach a design-conscious audience and increase interest in the event.',
      strategy='Partnered with niche home & lifestyle KOLs to create authentic, platform-native content that resonates with Malaysia’s Chinese-speaking audience.',
      stats=[('17,760','Total Reach'),('136,300','Total Followers Gained'),('522','Total Engagements')],gallery=['assets/img/cases/im-3.webp','assets/img/cases/im-1.webp','assets/img/cases/im-2.webp']),
 dict(slug='mummys-market-xiaohongshu',client='Mummys Market',cat='Xiaohongshu Marketing',industry='Baby & family fair',logo='assets/img/logos/mummys-market.png',image='assets/img/cases/mummys-market.webp',alt='Mummys Market Xiaohongshu campaign',
      desc='Targeted influencer marketing on XiaoHongShu to drive awareness and footfall for Mummys Market.',
      title='11 Influencer Posts and 65K+ Impressions for Mummys Market',
      challenge='Drive awareness and footfall for Mummys Market through targeted influencer marketing on XiaoHongShu (XHS).',
      strategy='MYSense selected parenting and lifestyle creators active on XHS, briefed them around the fair’s highlights and tracked reach, impressions and engagement across every post.',
      stats=[('11','Influencer Posts published'),('13K+','Total Reach'),('65K+','Total Impressions'),('1.5K+','Total Engagements')],gallery=['assets/img/cases/im-1.webp','assets/img/cases/im-3.webp','assets/img/cases/im-2.webp']),
]
for c in CASES: c['href']=f'/case-studies/{c["slug"]}/'

POSTS=[
 dict(title='5 Things to Do Now That AI Overviews Are Standard',date='October 6, 2026',image='assets/img/blog/ai-seo.svg',href='/insights/what-is-geo-ai-search/'),
 dict(title='How AI Search Is Changing the Way Brands Get Found',date='October 6, 2026',image='assets/img/blog/Screenshot-2026-07-28-at-11.31.44-Medium.jpeg',href='/insights/what-is-geo-ai-search/'),
 dict(title='What Is GEO? A Guide to Ranking in AI Search',date='October 5, 2026',image='assets/img/blog/seo-search-engine-optimization-concept-businessman-touch-ai-1.jpg',href='/insights/what-is-geo-ai-search/'),
 dict(title='5 Questions to Ask Before Hiring an AI SEO Provider',date='October 5, 2026',image='assets/img/blog/Screenshot-2026-07-28-at-10.39.54-Medium.jpeg',href='/insights/what-is-geo-ai-search/'),
 dict(title='How to Vet an AI SEO Agency: 4 Malaysian Providers Compared (2026)',date='October 4, 2026',image='assets/img/blog/Best-Agencies-for-Ranking-on-ChatGPT-AI-Search-2026.jpg',href='/insights/what-is-geo-ai-search/'),
 dict(title='5 AI Marketing Tools Malaysian Brands Actually Use',date='October 4, 2026',image='assets/img/blog/5-AI-Marketing-Tools-Malaysian-Brands-Actually-Use.jpg',href='/insights/what-is-geo-ai-search/'),
 dict(title='SEO, Google Ads or AI Search: Where to Focus in 2026?',date='October 3, 2026',image='assets/img/blog/SEO-Google-Ads-or-AI-Search-Where-to-Focus-in-2026.jpg',href='/insights/what-is-geo-ai-search/'),
 dict(title='5 Signs Your Website Isn’t Ready for AI Search',date='October 3, 2026',image='assets/img/blog/5-Signs-Your-Website-Isnt-Ready-for-AI-Search.jpg',href='/insights/what-is-geo-ai-search/'),
 dict(title='7 Landing Page Mistakes Killing Your Conversions',date='October 2, 2026',image='assets/img/blog/Screenshot-2026-07-22-at-13.15.09-Medium.jpeg',href='/insights/what-is-geo-ai-search/'),
]

REVIEWS=[
 dict(name='Marketing Uzma',role='Clinic marketing team',company='Google review',quote="We've been working with MYSense for our clinic's Google Ads, focusing mainly on our higher-margin services, and the results have been worthwhile."),
 dict(name='Aizat Anuar',role='SEO & SEM client',company='Google review',quote="Five stars for MYSense! They've been incredible at helping me navigate the world of SEO and SEM. They are honest, hardworking and most importantly, results-oriented."),
 dict(name='Irsen Woon',role='myRuma',company='myRuma',quote="MYSense has been nothing less than a great help to expand myRuma's reach in Meta, SEO and SEM. Special thanks to Emily and Ken for their continuous support, it's always a pleasure working with them."),
 dict(name='Nur Nazirah',role='Annur Eye Specialist Centre',company='Annur Eye Specialist Centre',quote="Best marketer for my business. My followers and likes increase together with messenger for appointment. Definitely recommended."),
 dict(name='HH Chee',role='White Perfect Dental',company='White Perfect Dental',quote="I am pleased with the professionalism and creative talent that has been provided all these while. Always communicate in timely manner and providing amazing ideas for the marketing posts."),
 dict(name='KYap Channel',role='SEO client',company='Google review',quote="Our website ranking has improved a lot since we started with them. Their SEO team really knows what they are doing and gave us great advice on how to optimize our content."),
 dict(name='Grace Ong Qiao Enn',role='Influencer marketing client',company='Google review',quote="Samantha has demonstrated strong pitching skills and provides excellent service throughout the project."),
 dict(name='Siew BeeBee',role='Dr Chong Clinic',company='Dr Chong Clinic',quote="Thank you WanLi and Samantha for helping out on my company to get influencers and they are working on their best to meet our expectation."),
]

FAQ_HOME=[
 ('How much do MYSense charge?','It depends on a few factors. The price is usually cost efficient and depends on the scale of your project. First of all, we will make a marketing proposal and showcase to you our proposed strategy to help you enhance your digital performance.'),
 ('Would my business benefit from digital marketing?','Definitely. Avoiding digital marketing denies your business access to the media the majority of consumers turn to first and at all hours of the day. We value collaboration with our clients by focusing on their organic growth through a great sense of authenticity.'),
 ('What if the results delivered are not what I am hoping for?','We will kickstart with a detailed business analysis for your company and make sure the outcome is of mutual consensus. Our team will ensure that we achieve the outcome discussed.'),
 ('Who has the ownership of all the materials produced?','You have the full ownership over the materials. If we part ways, you can request to send everything we have created for you in the contract period.'),
 ('What is the difference between SEO and GEO?','Traditional SEO gets your restaurant listed in the directory. GEO makes your restaurant the one the trusted food blogger recommends by name. Both are valuable, but GEO builds the authority that gets you directly recommended. A strong SEO foundation is the launching pad for a powerful GEO strategy.'),
 ('How long does it take to see SEO results?','Most businesses start seeing early improvements in 3–6 months, with stronger, more stable results from 6–12 months onwards. The exact timeline depends on your industry, competition, your website’s current condition and how aggressively we execute the SEO plan.'),
 ('How long does it take to see GEO results?','GEO is about building long-term authority, not overnight tricks. While foundational improvements can be seen within 1–2 months, most of our clients start seeing significant, measurable results, like a noticeable increase in qualified leads, within 4 to 6 months.'),
 ('Do you only work with businesses in Kuala Lumpur?','No. While we work with many businesses in Kuala Lumpur and Petaling Jaya, we also support clients across Malaysia and selected international markets. Our team is used to handling multi-location strategies.'),
]

SERVICES_ACC=[
 dict(title='Search Engine Optimisation (SEO)',desc='Improve your Google rankings, attract organic traffic, and generate consistent leads from search.',list=['Technical SEO audit & fixes','Keyword research (English, BM, Chinese)','Google Business Profile optimisation','Monthly ranking & traffic report'],image='assets/img/services/seobg-v2.webp',href='/services/seo/'),
 dict(title='Generative Engine Optimisation (GEO)',desc='Increase your brand visibility across AI search platforms like ChatGPT, Gemini, and other generative engines.',list=['AI visibility audit across major AI assistants','Answer-ready content & FAQ structuring','Schema markup & entity optimisation','Monthly AI citation & share-of-voice report'],image='assets/img/services/geo-ai.jpg',href='/services/geo/'),
 dict(title='Search Engine Marketing (SEM)',desc='Reach customers instantly with targeted Google Ads campaigns designed to drive high-quality conversions.',list=['Campaign & landing page setup','GA4 and conversion tracking','Weekly bid and keyword optimisation','Monthly cost-per-lead reporting'],image='assets/img/services/sembg-v2.webp',href='/services/sem/'),
 dict(title='Social Media Marketing & Management',desc='Build brand awareness, engage your audience, and grow your social presence with strategic content and campaigns.',list=['Monthly content calendar','Graphic design & short-form video','Paid social (Meta & TikTok Ads)','Copywriting'],image='assets/img/services/smmbg-v2.webp',href='/services/social-media-marketing/'),
 dict(title='Influencer Marketing & KOL Campaigns',desc='Partner with the right influencers to build trust, expand reach, and drive authentic engagement for your brand.',list=['Creator shortlist from our network','Campaign brief & content approval','Usage rights & contracts','Post-campaign performance report'],image='assets/img/services/imbg-v2.webp',href='/services/influencer-marketing/'),
 dict(title='Website Development & Design',desc='Create high-performing, SEO-friendly websites designed to convert visitors into leads and customers.',list=['Custom design, no templates','Mobile-first & Core Web Vitals ready','Lead forms, WhatsApp & CRM hooks','SEO & GEO built-in'],image='assets/img/services/webbg-v2.webp',href='/services/web-development/'),
]

VIDS=[('3dRbj5mUtDY','MYSense × Klinik Suzana (Aesthetic)','testimonial-1.jpg'),('ZQgHSabAufM','MYSense × Rejuve Clinic (Aesthetic)','testimonial-2.jpg'),('roRaIJw5caw','MYSense × Cellesis (Aesthetic)','testimonial-3.jpg'),('e2XYqIlezUk','MYSense × La Jung (Aesthetic)','testimonial-4.jpg'),('QuPSpksVtmw','MYSense × myTukar (Car selling)','testimonial-5.jpg'),('3GDPSnC8t4c','MYSense × Annur Eye Clinic','testimonial-6.jpg'),('a1r2JwLxNso','MYSense × BAAGUS (Home furnishing)','testimonial-7.jpg'),('oLO7LlDNeCM','MYSense × ESONA (Healthcare)','testimonial-8.jpg')]
def video_section(root, n=4, lbl='Client Stories', title='Hear It From Our Clients'):
    vg=''.join(f'<a class="vcard rv" href="https://www.youtube.com/watch?v={v}" target="_blank" rel="noopener" aria-label="{esc(t)}"><img src="{root}assets/img/videos/{f}" alt="{esc(t)}" loading="lazy"><i>{PLAY}</i></a>' for v,t,f in VIDS[:n])
    return section(f'<div class="head-row"><div class="head-stack" style="max-width:600px"><div class="rv">{label(lbl)}</div><h2 class="t-h2 rv">{title}</h2></div><div class="rv">{alink("Watch all client stories", root+"testimonials/")}</div></div><div class="video-grid" data-stagger="0.06">{vg}</div>','section section--phone70')

def testimonials_section(root, lbl='Reviews', title='What Our Clients Say'):
    return section(f'''<div class="head-row head-row--testi"><div class="head-stack" style="max-width:464px"><div class="rv">{label(lbl)}</div><h2 class="t-h2 rv">{title}</h2></div>
<div class="arrows rv"><button data-prev aria-label="Previous">{ARROW_L}</button><button data-next aria-label="Next">{ARROW_R}</button></div></div>
<div class="slider rv"><div class="slider__track">{''.join(tcard(t,root) for t in REVIEWS)}</div></div>''')

def faq_section(root, items, lbl='FAQ', title='Frequently Asked Questions', help=True):
    hb=f'''<div class="faq__help rv"><div><p class="t-19">Can’t find what you’re looking for?</p><p class="desc">Reach out anytime, we’re happy to help.</p>
<div class="person"><div><p>WhatsApp <a href="{C.SITE['phone_href']}">+6019-3541688</a></p><p class="t-small">{C.SITE['email']}</p></div></div></div>
{alink('Email Us','mailto:'+C.SITE['email'])}</div>''' if help else ''
    return section(f'<div class="faq"><div class="faq__left"><div class="head-stack"><div class="rv">{label(lbl)}</div><h2 class="t-h2 rv">{title}</h2></div>{hb}</div>{faq(items)}</div>','section section--phone70')

def insights_section(root, posts=POSTS[:3]):
    return section(f'''<div class="head-row"><div class="ins-head__left"><div class="rv">{label('Blog')}</div><h2 class="t-h2 rv">Latest Insights</h2><p class="t-body rv">Explore the latest insights and digital marketing articles from the MYSense team.</p></div><div class="rv">{alink('Read More', root+'insights/')}</div></div>
<div class="ins"><div class="ins__col">{post_big(posts[0],root)}</div><div class="ins__col">{post_sm(posts[1],root)}{post_sm(posts[2],root)}</div></div>''','section section--phone70')

def clients_section(root, logos=LOGOS_HOME, est='300+ brands served'):
    return section(clients_strip(root, logos, est),'clients')

# ======================================================================
def home(root):
    hero=f'''<section class="hero"><div class="wrap">
  <div class="hero__top">
    <div class="hero__left"><h1 class="t-h1 hero__h1 rv-hero d1">Digital Marketing Agency Malaysia</h1><p class="hero__sub rv-hero d2"><b>Data-Driven Marketing</b> That Helps Businesses <span class="rotator"><span>Grow</span><span>Scale</span><span>Escalate</span></span></p><div class="rv-hero d2">{btn('Get a Free Consultation','#general-form')}</div></div>
    <div class="rv-hero d2">{trust([root+a for a in AV])}</div>
  </div>
  <div class="hero__tags rv-hero d3"><span>SEO &amp; GEO</span><span>Google Ads &amp; Social Media</span><span>Influencer Marketing</span></div>
  <div class="hero__media rv-hero d4"><video src="{root}assets/video/herob.mp4" autoplay muted loop playsinline poster="{root}assets/img/misc/hero-poster.jpg"></video><button class="hero__pause" aria-label="Pause video"></button></div>
</div></section>'''
    cases=section(head_split('Our Works','Case Studies','Join brands that have already transitioned to data-driven growth.')+f'<div class="case-grid">{"".join(case_card(c,root) for c in CASES[:4])}</div>')
    who=section(f'''<div class="head-split"><div class="rv">{label('Who We Are')}</div><div class="who__right">
  <span class="who__brand rv"><img src="{root}assets/img/brand/logo_black_mark.png" alt="" style="height:20px"></span>
  <p class="t-quote words scrub">MYSense is a data-driven digital marketing agency based in Petaling Jaya, Malaysia. We specialise in SEO, GEO, Paid Ads, Social Media Marketing, Influencer Marketing, and Website Development to help brands grow in today’s competitive digital landscape.</p>
  <div class="rv">{alink('Learn More', root+'about/')}</div></div></div>
<div class="who__cards">
  <div class="person-card rv"><div class="person-card__img"><img src="{root}assets/img/brand/award-stage.webp" alt="The MYSense team on stage as Search Agency of the Year 2026 is announced" loading="lazy"><span class="person-card__ic">{STAR}</span></div><div class="person-card__cap"><p class="t-19">Search Agency of the Year 2026</p><p class="muted">Silver award</p></div></div>
  <div class="who__spacer"></div>
  <div class="who__pair">
    <div class="mini mini--light rv"><h3 class="t-h1">300+</h3><div class="mini__avatars">{avatars([root+a for a in AV])}</div><p class="t-19 mini__cap">Brands Served Across Malaysia</p>{btn('Get Your Free Strategy Plan','#general-form', full=True)}</div>
    <div class="mini mini--dark rv"><div class="mini__top"><h3 class="t-h1">GEO</h3><span class="chevrons">{CHEVRON}{CHEVRON}{CHEVRON}</span></div><p><strong style="color:#fff">New: Generative Engine Optimisation.</strong> Get your brand recommended by AI when customers ask ChatGPT, Gemini, Perplexity or Google AI Overviews. <a href="{root}services/geo/" style="color:var(--card-2);text-decoration:underline">Learn more</a></p></div>
  </div>
</div>''')
    process=section(head_stack('Process','Our Working Process',maxw=733)+f'''<div class="process">
  <div class="process__img rv"><img src="{root}assets/img/about-team.jpg" alt="The MYSense team" loading="lazy"><p class="t-h2">MYSense</p><div><p class="t-tiny">300+ brands served</p><p class="t-19" style="margin-top:10px">Our Working Process</p></div></div>
  {steps([('Discovery & Strategy','We begin by understanding your business, industry, competitors, and target audience to develop the right digital marketing strategy.'),('Planning & Campaign Setup','Our team designs a tailored digital marketing plan, selecting the most effective channels such as SEO, Paid Ads, Social Media, or Influencer Marketing.'),('Execution & Optimization','We launch and manage your campaigns while continuously analysing performance data to optimize results.'),('Reporting & Growth','Transparent performance reports allow us to track progress, refine strategies, and scale campaigns for sustainable business growth.')])}
</div>''')
    services=section(f'<div class="panel rv">{head_stack("Services","Our Digital Marketing Services in Malaysia",light=True,maxw=640)}{accordion(SERVICES_ACC,root)}</div>','section section--tight')
    results=section(f'''<div class="head-row"><div class="head-stack" style="max-width:420px"><div class="rv">{label('Our Impact')}</div><h2 class="t-display rv">Results</h2></div><div class="rv">{btn('Get Your Free Strategy Plan','#general-form')}</div></div>
<div class="stat-grid" data-stagger="0.08">{stat_card('300','+','Brands Served','300+ brands across healthcare, automotive, finance, F&B, retail, property and education trust MYSense with their digital marketing.')}{stat_card('96','%','Client Retention Rate','A full team managing your brand daily: project manager, strategists, designers and ads specialists supporting your growth.')}{stat_card('120','+','5-Star Google Reviews','Rated 4.9 on Google by the clients we work with every day, across SEO, Google Ads, social media and influencer campaigns.')}{stat_card('30','%+','Average Increase In ROI','We prioritise initiatives based on impact and ROI, leverage market trends and competitor analysis, and A/B test to optimise campaigns.')}</div>''')
    plans=section(head_split('Get Started','Start With MYSense','Whether you need a second opinion on your marketing or a partner to deliver under your brand, there is a simple way to begin.',display=True).replace('t-19 rv','t-body rv')+f'''<div class="plans">
  <div class="plan rv"><p class="plan__name">Free Strategy Session</p><p class="plan__h">Claim your free digital marketing strategy session, <span>worth RM3,000</span></p>
    <div class="plan__price"><span class="pre">RM</span><span class="big">3,000</span><span class="suf">value, free</span></div>{btn('Worth RM3,000 — Claim for free now!','#general-form')}
    <div class="plan__div"></div><ul class="plan__feats">{''.join(f'<li>{PLUS}{esc(x)}</li>' for x in ['30-minute strategy session','Website review','Ads & social review','3 changes to bring in more leads','Reply within 1-2 working days','Clear RM pricing, no lock-in surprises'])}</ul></div>
  <div class="plan plan--dark rv"><p class="plan__name">White Label Partnership</p><p class="plan__h">Scale your agency without hiring more staff, <span>delivered under your brand</span></p>
    <div class="plan__price"><span class="big">300+</span><span class="suf">brands served</span></div>{btn('Book A Partnership Call', root+'white-label/', light=True)}
    <div class="plan__div"></div><ul class="plan__feats">{''.join(f'<li>{PLUS}{esc(x)}</li>' for x in ['SEO & SEM delivery','Social media management','Influencer marketing','Website development','Increase profit margins','Expand service offerings','Save manpower cost','Reduce operational risk'])}</ul></div>
</div>''')
    body=hero+clients_section(root)+cases+who+process+services+results+testimonials_section(root)+video_section(root)+plans+faq_section(root,FAQ_HOME)+insights_section(root)+contact_band(root,'assets/img/misc/mysense-photo.jpg',text="Tell us a little about your business and we’ll get back to you within 1-2 working days.",direct_btn=('Let’s Talk Now!','https://wa.me/60193541688'))
    return body

# ======================================================================
CONTAIN=' style="object-fit:contain;background:#fff;padding:32px"'
def about(root):
    hero=f'''<section class="page-hero"><div class="wrap">
  <div class="rv-hero d1">{label('About Us')}</div>
  <div class="about-hero__row"><div><h1 class="t-display rv-hero d2" style="margin-top:32px">Inside MYSense</h1><div class="rv-hero d3">{trust([root+a for a in AV],strong='300+ brands in Malaysia')}</div></div>
  <p class="t-19 about-hero__p rv-hero d3">A data-driven digital marketing agency based in Petaling Jaya, Malaysia, specialising in SEO, Paid Ads, Social Media Marketing, Influencer Marketing and Website Development.</p></div>
  <div class="big-img rv-hero d4"><img src="{root}assets/img/about-team.jpg" alt="The MYSense team"></div>
  <div class="about-stats"><div class="stat-grid" data-stagger="0.08">{stat_card('5','+','Years in Business',short=True)}{stat_card('40','+','Employees',short=True)}{stat_card('300','+','Brands Served',short=True)}{stat_card('120','+','5-Star Google Reviews',short=True)}</div></div>
</div></section>'''
    story=section(f'''<div class="two-col"><div class="rv">{label('Our Story')}</div><div class="two-col__right">
<p class="t-24 words scrub">MYSense started as a passionate team focused on helping healthcare businesses navigate the digital landscape. Through years of experience working closely with medical and healthcare brands, we developed strong expertise in building digital strategies that increase visibility, strengthen brand trust, and drive sustainable growth.</p>
<p class="t-24 rv"><span>As the market evolved and more industries recognised the power of digital marketing, MYSense expanded its capabilities to support businesses across healthcare, education, F&amp;B, finance, automotive, and beyond. Today, we continue to help brands grow with data-driven marketing strategies designed to attract the right audience, generate leads, and deliver measurable business impact.</span></p></div></div>
<div class="two-col" style="margin-top:100px"><div class="rv">{label('Our Vision')}</div><div class="two-col__right"><p class="t-24 words scrub">To empower businesses to grow and compete in the digital world through smarter, data-driven marketing strategies.</p>
<p class="t-24 rv"><span>At MYSense, our culture is built on P.A.I. — People First, Achiever, and Integrity — guiding how we collaborate, innovate, and deliver meaningful results for our clients.</span></p></div></div>''')
    awards=[('SOBA 2022','The Star Outstanding Business Awards','assets/img/misc/soba-2023.jpg'),('SME Rising Star Award','Winner','assets/img/misc/sme-award.jpg'),('Search Agency of the Year 2026','Silver award','assets/img/brand/award-stage.webp'),('Malaysia Book of Records 2026','Most healthcare brand clients managed by a digital marketing agency','assets/img/brand/award-mbor-team.jpg')]
    team=section(head_stack('Recognised for Excellence','We Are Committed To Help Your Business Succeed',cls='t-h1',maxw=760)+'<div class="team-grid" data-stagger="0.08">'+''.join(f'<div class="team-card rv"><img src="{root}{i.split("|")[0]}" alt="{esc(t)}" loading="lazy"{CONTAIN if "|contain" in i else ""}><div class="team-card__cap"><p class="t-19">{esc(t)}</p><p class="r">{esc(s)}</p></div></div>' for t,s,i in awards)+'</div>')
    expertise=section(head_stack('Our Expertise','What We Do',maxw=600)+'<div class="logo-grid" data-stagger="0.06">'+''.join(f'<a class="logo-card rv" href="{root}{h.lstrip("/")}" style="filter:none;flex-direction:column;gap:6px;color:var(--ink)"><span class="t-19">{esc(t)}</span><span class="t-small muted">{esc(s)}</span></a>' for t,s,h in [('SEO','Search Engine Optimisation','/services/seo/'),('GEO','Generative Engine Optimisation','/services/geo/'),('SEM','Search Engine Marketing','/services/sem/'),('Social Media','Management & Ads','/services/social-media-marketing/'),('Influencer Marketing','KOL campaigns','/services/influencer-marketing/'),('Website Development','Design & build','/services/web-development/'),('Xiaohongshu','XHS marketing','/services/xiaohongshu-marketing/'),('TikTok','Official partner','/services/tiktok-marketing/')])+'</div>')
    clients=section(clients_strip(root,LOGOS_ABOUT,'300+ brands served')+f'<div class="photo-row rv"><img src="{root}assets/img/team/life-1.webp" alt="Team building" loading="lazy"><img src="{root}assets/img/team/life-2.webp" alt="Company trip" loading="lazy"><img src="{root}assets/img/team/life-4.webp" alt="Annual dinner" loading="lazy"></div>','section')
    return hero+story+team+expertise+clients+cta_panel('Get A Free Evaluation Of Your Current Digital Marketing Strategy','Discover opportunities to grow your business online.',"Let’s Talk Now!",'/contact/',root)

# ======================================================================
def contact(root):
    return f'''<section class="page-hero page-hero--center"><div class="wrap">
  <div class="rv-hero d1">{label('Talk To Our Experts Today!')}</div><h1 class="t-display rv-hero d2" style="margin-top:24px">Contact Us</h1>
  <div class="book rv-hero d3" style="text-align:left">
    <div class="book__img"><img class="bg" src="{root}assets/img/misc/team-meeting.webp" alt=""><h2 class="t-h2">Claim your free digital marketing strategy session, worth RM3,000</h2>
      <div class="book__quote"><p>“Five stars for MYSense! They provide clear data and numbers so you always know exactly how your investment is performing.”</p><div class="who"><span style="width:45px;height:45px;border-radius:999px;background:var(--card);color:var(--ink);display:inline-flex;align-items:center;justify-content:center;font-weight:600">A</span><div><p>Aizat Anuar</p><p class="t-small r">Google review</p></div></div></div></div>
    <div class="book__body">{trust([root+a for a in AV],strong='300+ brands in Malaysia')}<p>Book a free 30-minute strategy session. We’ll review your website, ads and social, and show you the 3 changes most likely to bring in more leads. We get back to you within 1-2 working days.</p>
      <form class="embed" data-mock>
        <div class="field"><label for="c-name">Name</label><input id="c-name" type="text" placeholder="Your name" required></div>
        <div class="field"><label for="c-email">Company email</label><input id="c-email" type="email" placeholder="you@company.com" required></div>
        <div class="field"><label for="c-phone">WhatsApp number</label><input id="c-phone" type="tel" placeholder="+60"></div>
        <div class="field"><label for="c-svc">Service you are interested in</label><select id="c-svc"><option>Search Engine Optimisation</option><option>Generative Engine Optimisation</option><option>Google Ads (SEM)</option><option>Social Media Marketing</option><option>Influencer Marketing</option><option>Website Development</option><option>Not sure yet</option></select></div>
        <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" placeholder="Tell us a little about your business"></textarea></div>
        <button class="btn btn--submit" type="submit">Talk To Our Experts Today!</button>
        <p class="t-small muted">Don’t have a company email? No problem, new businesses can reach us with any email address.</p>
      </form></div>
  </div>
</div></section>''' + section(f'''<div class="two-col"><div class="rv">{label('Head Office')}</div><div class="two-col__right">
<p class="t-24 rv">{esc(C.SITE['address'])}</p><p class="t-24 rv"><a class="rollhost" href="{C.SITE['phone_href']}">{roll('+6019-3541688')}</a> · <a class="rollhost" href="mailto:{C.SITE['email']}">{roll(C.SITE['email'])}</a></p>
<div class="rv" style="border-radius:12px;overflow:hidden;aspect-ratio:16/8;background:var(--g-300)"><iframe title="MYSense on Google Maps" src="https://maps.google.com/maps?q=MYSense%20%28SEO%20%7C%20Social%20Media%20%7C%20Influencer%20Marketing%20Agency%20in%20Petaling%20Jaya%29&t=m&z=15&output=embed&iwloc=near" style="border:0;width:100%;height:100%" loading="lazy"></iframe></div></div></div>''') + faq_section(root,FAQ_HOME[:4],help=False)

# ======================================================================
def case_hub(root):
    return f'''<section class="page-hero"><div class="wrap">{head_split('Our Works','Case Studies','Join brands that have already transitioned to data-driven growth. A closer look at how we rank, convert and scale Malaysian brands with SEO, Google Ads, social media and influencer marketing.').replace('rv"','rv-hero d2"')}
<div class="case-grid">{''.join(case_card(c,root) for c in CASES)}</div></div></section>'''+cta_panel('Be The Next Success Story.','Tell us about your brand and we will map out the strategy, channels and budget that fit your goals.',"Let’s Talk Now!",'/contact/',root)

def case_detail(c):
    def b(root):
        others=[x for x in CASES if x is not c][:2]
        meta=f'''<div class="meta-bar rv"><div class="m"><span class="k">Scope of work</span><div class="v"><span>{esc(c['cat'])}</span></div></div><div class="m"><span class="k">Industry</span><div class="v"><span>{esc(c['industry'])}</span></div></div><div class="m"><span class="k">Client</span><div class="v"><span>{esc(c['client'])}</span></div></div><div class="m right"><span class="k">All Case Studies</span><div class="v">{alink('View all', root+'case-studies/')}</div></div></div>'''
        logo=f'<img src="{root}{c["logo"]}" alt="{esc(c["client"])}" style="height:50px;width:auto;max-width:156px;object-fit:contain">' if c.get('logo') else ''
        stats=''.join(f'<div class="stat-box rv"><span class="stat-box__v">{esc(v)}</span><span class="stat-box__l">{esc(l)}</span></div>' for v,l in c['stats'])
        return f'''<section class="page-hero"><div class="wrap">
  <a class="back rv-hero d1" href="{root}case-studies/"><i>{ARROW_L}</i>Back To Case Studies</a>
  <div class="page-hero__row" style="margin-top:32px"><div><h1 class="t-h1 rv-hero d2">{esc(c['title'])}</h1><p class="t-19 page-hero__sub rv-hero d3">{esc(c['desc'])}</p></div><div class="rv-hero d3">{logo}</div></div>
  {meta}
  <div class="hero-img rv"><img src="{root}{c['image']}" alt="{esc(c['alt'])}"></div>
</div></section>
{section(f'<div class="block"><div class="rv">{label("Challenges")}</div><div class="block__txt"><p class="t-24 words scrub">{esc(c["challenge"])}</p></div></div><div class="block"><div class="rv">{label("Our Strategy")}</div><div class="block__txt"><p class="t-24 words scrub">{esc(c["strategy"])}</p></div></div>')}
{section('<div class="img-stack">'+''.join(f'<img class="rv" src="{root}{g}" alt="" loading="lazy">' for g in c['gallery'])+'</div>','section section--tight')}
{section(f'<div class="results-row"><div class="rv">{label("Results")}</div><div class="boxes">{stats}</div></div>')}
{section(f'<div class="head-split"><div class="rv">{label("Projects")}</div><h2 class="t-h1 rv" style="text-align:right">More Projects</h2></div><div class="case-grid">{"".join(case_card(o,root) for o in others)}</div>')}'''
    return b

# ======================================================================
def insights(root):
    return f'''<section class="page-hero"><div class="wrap">{head_split('Insights, Strategies &amp; Perspectives','Insights','Explore the latest insights and digital marketing articles from the MYSense team on SEO, GEO, Google Ads, social media and influencer marketing in Malaysia.').replace('rv"','rv-hero d2"')}
<div class="case-grid" style="gap:20px">{''.join(post_sm(p,root) for p in POSTS)}</div></div></section>'''

def post(root):
    body=md_prose('blog-samples/what-is-geo-ai-search', drop_until=None)
    # strip the repeated title + nav junk at top by cutting to the first real paragraph
    return f'''<article class="article">
  <a class="back rv-hero d1" href="{root}insights/"><i>{ARROW_L}</i>Back To Insights</a>
  <div class="article__meta rv-hero d2"><p class="d">Sunday, October 5, 2026</p><h1 class="t-h2">What Is GEO? A Guide to Ranking in AI Search</h1>
    <div class="article__by"><p class="t-small">Posted by</p><div class="who"><img src="{root}assets/img/brand/favicon.png" alt=""><div><p>MYSense Team</p><p class="t-small muted">Digital Marketing Agency Malaysia</p></div></div></div></div>
  <div class="article__img rv-hero d3"><img src="{root}assets/img/blog/seo-search-engine-optimization-concept-businessman-touch-ai-1.jpg" alt=""></div>
  <div class="prose rv">{body}</div>
</article>'''+insights_section(root,POSTS[3:6])

# ======================================================================
def legal(slug, title):
    def b(root):
        return f'<div class="wrap"><div class="legal"><h1 class="t-h1 rv-hero d1">{esc(title)}</h1><div class="prose rv-hero d2">{md_prose(slug)}</div></div></div>'
    return b

def job_scam(root):
    return f'<div class="wrap"><div class="legal"><div class="rv-hero d1">{label("Important notice")}</div><h1 class="t-h1 rv-hero d1" style="margin-top:24px">Beware of Job Scams</h1><div class="prose rv-hero d2">{md_prose("job-scam")}</div><p class="rv">{btn("Career", root+"career/")}</p></div></div>'

# ======================================================================
def build_core():
    if os.path.isdir(os.path.join(SITE,'assets','css')): pass
    os.makedirs(os.path.join(SITE,'assets','css'),exist_ok=True); os.makedirs(os.path.join(SITE,'assets','js'),exist_ok=True)
    shutil.copy(os.path.join(HERE,'src','main.css'),os.path.join(SITE,'assets','css','main.css'))
    shutil.copy(os.path.join(HERE,'src','main.js'),os.path.join(SITE,'assets','js','main.js'))
    write('/','Digital Marketing Agency Malaysia | Data-Driven MYSense','MYSense is a digital marketing agency in Malaysia trusted by 300+ brands for SEO, GEO, and social media growth. Book a free strategy call.',home)
    write('/about/','About MYSense — Malaysia’s Digital & Influencer Marketing Agency','MYSense is a data-driven digital marketing agency based in Petaling Jaya, Malaysia, specialising in SEO, Paid Ads, Social Media, Influencer Marketing and Website Development.',about)
    write('/contact/','Contact Us | MYSense Digital Marketing Agency Malaysia','Talk to our experts today. Claim your free digital marketing strategy session worth RM3,000.',contact)
    write('/case-studies/','Case Studies | MYSense','SEO, Google Ads, social media and influencer marketing results for Malaysian brands.',case_hub)
    for c in CASES: write(c['href'],f'{c["client"]} — {c["cat"]} Case Study | MYSense',c['desc'],case_detail(c))
    write('/insights/','Digital Marketing Malaysia | Insights | MYSense','Explore the latest insights and digital marketing articles from MYSense.',insights)
    write('/insights/what-is-geo-ai-search/','What Is GEO? A Guide to Ranking in AI Search | MYSense','MYSense explains what GEO actually is, how it differs from SEO, and how to start ranking in AI search.',post)
    write('/privacy-policy/','Privacy Policy | MYSense','MYSense privacy policy.',legal('privacy-policy','Privacy Policy'))
    write('/terms-of-services/','Terms of Services | MYSense','MYSense terms of services.',legal('terms-of-services','Terms of Services'))
    write('/quality-policy/','Quality Policy | MYSense','MYSense quality policy.',legal('quality-policy','Quality Policy'))
    write('/job-scam/','Beware of Job Scams | MYSense','MYSense does not offer part-time jobs through social media.',job_scam)

def mirror():
    dst='/private/tmp/claude-501/-Users-mysense-Desktop/7822ac80-5e0b-490b-9c19-29b6d6d977bd/scratchpad/site_serve'
    os.makedirs(dst,exist_ok=True)
    for root_,dirs,files in os.walk(SITE):
        r=os.path.relpath(root_,SITE); d=os.path.join(dst,r); os.makedirs(d,exist_ok=True)
        for f in files:
            s_=os.path.join(root_,f); t=os.path.join(d,f)
            if not os.path.exists(t) or os.path.getmtime(s_)>os.path.getmtime(t) or os.path.getsize(s_)!=os.path.getsize(t): shutil.copy2(s_,t)
    print('mirrored to',dst)

if __name__=='__main__':
    build_core()
    try:
        import gen_pages; gen_pages.build(write)
    except ImportError as e:
        print('gen_pages not present yet:', e)
    mirror()
