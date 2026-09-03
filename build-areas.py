# -*- coding: utf-8 -*-
"""Generates the /areas index and one page per Riyadh district we name on the site.
Each page is written by hand below — no spun text — because thin near-duplicate
location pages are exactly what search engines discount."""
import re, io, os

SPRITE = re.search(r'<svg class="brand-sprite".*?</svg>', open('index.html').read(), re.S).group(0)

D = [
 dict(slug='diriyah', file='area-diriyah.html', name='Diriyah', img='diriyah.jpg',
   co='24.73 N · 46.57 E',
   title='Personal Training in Diriyah, Riyadh | ONE Wellness',
   meta='Private in-home personal training in Diriyah with Olympic medallists Aaron and Bianca Cook. We bring the session to your door.',
   lede='Heritage on one side, one of the most ambitious developments in the Kingdom on the other. Diriyah is changing fast, and the people moving into it tend to be building something themselves.',
   character='Diriyah holds At-Turaif, the mud-brick quarter where the first Saudi state began and now a UNESCO World Heritage Site. Around it, Bujairi Terrace and a wave of new residences have brought a very different pace. Wadi Hanifah runs alongside, which means residents here already have somewhere green to walk and run — a rarity in the city.',
   space='Homes here range from established family villas to brand-new residences still being fitted out. If your gym is not built yet, that is not a problem: we have programmed around an empty garage and a set of dumbbells more than once, and we bring what the room is missing.',
   note='If you already walk Wadi Hanifah, we will build around it rather than ignore it — the easiest habit to keep is the one you already have.'),

 dict(slug='diplomatic-quarter', file='area-dq.html', name='Diplomatic Quarter', img='dq.jpg',
   co='24.68 N · 46.62 E',
   title='Personal Training in the Diplomatic Quarter, Riyadh | ONE Wellness',
   meta='Discreet private personal training in the Diplomatic Quarter (DQ), Riyadh. Olympic-level coaching in your own home, on your schedule.',
   article='the ',
   lede='The DQ was designed for privacy, and the people who live here expect it. So do we.',
   character='Low-rise, walled, landscaped and green, the Diplomatic Quarter is unlike anywhere else in Riyadh. Its walking paths and parks are among the best in the city, and the district is built at a human scale rather than a motorway one. Residents include diplomatic staff and families who value not being on display.',
   space='Housing in the DQ is a mix of compound villas, townhouses and apartments, often with shared facilities. We can work in your own home or in your compound gym, and we are used to arranging access quietly and in advance.',
   note='Discretion is not an add-on here. No cameras, no social posts, no client names — the same standard we apply everywhere, but it matters more in this postcode.'),

 dict(slug='hittin', file='area-hittin.html', name='Hittin', img='hittin.jpg',
   co='24.76 N · 46.60 E',
   title='Personal Training in Hittin, Riyadh | ONE Wellness',
   meta='Private in-home personal training in Hittin, Riyadh, with Olympic medallists Aaron and Bianca Cook. Training, nutrition and habits built around you.',
   lede='Large homes, young families, and not much spare time. Hittin is where the commute to a gym costs more than the session.',
   character='One of north-west Riyadh’s newer affluent districts, Hittin is largely low-density villa housing, close to Wadi Hanifah and a short drive from the Diriyah developments. It is residential in the truest sense — people come home here rather than pass through.',
   space='Most Hittin homes have more usable space than their owners realise: a majlis that is empty on weekday mornings, a garage, a shaded stretch of garden. We look at what you have before suggesting you buy anything.',
   note='Families are common here, and so are split sessions — one parent early, one later, same programme logic, different execution.'),

 dict(slug='al-malqa', file='area-malqa.html', name='Al Malqa', img='malqa.jpg',
   co='24.80 N · 46.61 E',
   title='Personal Training in Al Malqa, Riyadh | ONE Wellness',
   meta='Private personal training in Al Malqa, Riyadh. In-home coaching from Olympic medallists, built around your equipment and your week.',
   lede='Close to KAFD, full of people whose calendars move without warning. Al Malqa needs training that survives a changed schedule.',
   character='Al Malqa sits in northern Riyadh, near the King Abdullah Financial District, and has grown quickly into a district of modern villas and newer apartment buildings. It attracts professionals and young families — people early in a long career rather than at the end of one.',
   space='A newer build often means a compact but well-specified space: a home gym room with a rack and not much else, or an apartment with a shared facility downstairs. Both work. We programme for the equipment in front of us.',
   note='If your week genuinely cannot be predicted, say so at the introduction. We would rather design a programme that bends than one you abandon in a fortnight.'),

 dict(slug='al-nakheel', file='area-nakheel.html', name='Al Nakheel', img='nakheel.jpg',
   co='24.75 N · 46.64 E',
   title='Personal Training in Al Nakheel, Riyadh | ONE Wellness',
   meta='Private in-home personal training in Al Nakheel, Riyadh. Olympic-level coaching delivered to your door, on your schedule.',
   lede='Well connected, centrally placed, and busy. Al Nakheel is the district where "I will go later" quietly becomes "I did not go".',
   character='Al Nakheel sits in north-central Riyadh, close to King Fahd Road and within easy reach of the financial district. It is a mixed district of villas and apartment buildings, popular precisely because it is close to everything.',
   space='Being central often means less square footage, not more. That is fine — a corridor, a living room and a set of adjustable dumbbells is a real training environment when the programme is written for it.',
   note='Being close to a gym is not the same as going to one. The whole point of this service is removing the twenty minutes that stop you.'),

 dict(slug='al-olaya', file='area-olaya.html', name='Al Olaya', img='olaya.jpg',
   co='24.69 N · 46.68 E',
   title='Personal Training in Al Olaya, Riyadh | ONE Wellness',
   meta='Private personal training in Al Olaya, Riyadh. Apartment and penthouse coaching from Olympic medallists Aaron and Bianca Cook.',
   lede='Kingdom Centre, Al Faisaliah, and a lot of people working hours that make a gym membership decorative.',
   character='Al Olaya is central Riyadh’s business district — towers, hotels, offices and high-rise residential, with the Kingdom Centre and Al Faisaliah Tower on its skyline. Residents here are more likely to live in an apartment than a villa, and more likely to be time-poor than space-rich.',
   space='Apartment training is its own discipline. Downstairs facilities are often better than people assume, and where they are not, a well-chosen kit list and a floor plan will do more than a membership. Noise and neighbours are part of the design, not an afterthought.',
   note='Early mornings and late evenings are normal here. Sessions are booked around your working day, not the other way round.'),
]

NAV_LINKS = [('/story','Their story'),('/online-coaching','Online coaching'),('/areas','Areas we cover')]

def nav_html(active=''):
    out = []
    for href, label in NAV_LINKS:
        cur = ' aria-current="page"' if href == active else ''
        out.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    return '\n      '.join(out)

def head(title, meta, canonical):
    return '''<meta charset="utf-8">
<title>%s</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="%s">
<link rel="canonical" href="https://golden-oath-site.lovable.app%s">
<link rel="icon" href="assets/brand/favicon.png">
<link rel="preconnect" href="https://raw.githubusercontent.com" crossorigin>\n<link rel="dns-prefetch" href="https://raw.githubusercontent.com">\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Karla:wght@400;500;600&display=swap">''' % (title, meta, canonical)

print("module ready")

CSS = '''<style>
:root{--forest:#162E21;--forest-deep:#0F2018;--cream:#FBF9F5;--bone:#F7F3EC;--sand:#EDE4D6;
 --taupe:#9F876F;--sage:#BEC3A3;--ink:#221F1B;--champagne:#E3D3B3;--champagne-lt:#F2E8D5;
 --gold:#C4A468;--bronze:#A88756;--serif:'Cormorant Garamond',Georgia,serif;--sans:'Karla',Arial,sans-serif;
 --ease:cubic-bezier(.22,.9,.24,1)}
*{margin:0;padding:0;box-sizing:border-box;border-radius:0}
html{scroll-behavior:smooth}
body{background:var(--bone);color:var(--ink);font-family:var(--serif);font-size:19px;line-height:1.6;
 -webkit-font-smoothing:antialiased;overflow-x:hidden;position:relative}
body::before{content:"";position:fixed;inset:0;z-index:-2;pointer-events:none;
 background:radial-gradient(ellipse 70% 55% at 12% 8%,rgba(242,232,213,.95),transparent 62%),
  radial-gradient(ellipse 60% 50% at 88% 22%,rgba(227,211,179,.85),transparent 64%),
  radial-gradient(ellipse 80% 60% at 50% 62%,rgba(237,228,214,.9),transparent 70%),
  radial-gradient(ellipse 65% 55% at 8% 88%,rgba(196,164,104,.22),transparent 66%),
  linear-gradient(168deg,#FAF6EE,#F4EBDB 38%,#EFE3CC 68%,#E8DAC0)}
::selection{background:var(--forest);color:var(--cream)}
a{color:inherit}
:focus-visible{outline:1px solid var(--forest);outline-offset:4px}
img{max-width:100%;display:block}
.grain{position:fixed;inset:-50%;width:200%;height:200%;pointer-events:none;z-index:70;opacity:.032;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.k{font-family:var(--sans);font-weight:500;font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--taupe)}
.display{font-family:var(--serif);font-weight:300;font-style:italic;line-height:1.06;letter-spacing:-.01em;text-wrap:balance}
.wrap{max-width:1400px;margin:0 auto;padding:0 clamp(24px,4.5vw,64px)}
NAVCSS
/* hero */
.ahero{position:relative;min-height:74vh;display:flex;align-items:flex-end;background:var(--forest-deep);overflow:hidden}
.ahero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;
 filter:saturate(1.1) contrast(1.06);transform:translateZ(0)}
.ahero::after{content:"";position:absolute;inset:0;z-index:1;
 background:linear-gradient(180deg,rgba(15,32,24,.62),rgba(15,32,24,.3) 38%,rgba(15,32,24,.9) 84%,rgba(15,32,24,.97))}
.ahero .wrap{position:relative;z-index:2;padding-top:150px;padding-bottom:clamp(46px,8vh,86px)}
.ahero .k{display:block;margin-bottom:18px;color:var(--champagne)}
.ahero h1{font-size:clamp(36px,5vw,72px);color:var(--cream);max-width:14em}
.ahero .co{margin-top:18px;font-family:var(--sans);font-size:10px;font-weight:600;letter-spacing:.26em;
 text-transform:uppercase;color:var(--sage)}
/* body */
.asec{padding:clamp(76px,12vh,140px) 0}
.alede{font-family:var(--serif);font-style:italic;font-weight:300;font-size:clamp(24px,2.8vw,38px);
 color:var(--forest);max-width:21em;line-height:1.28}
.acols{display:grid;grid-template-columns:1fr 1fr;gap:clamp(30px,4.5vw,72px);margin-top:clamp(40px,6vh,64px)}
.acols h2{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(22px,2.1vw,30px);
 color:var(--forest);margin-bottom:14px}
.acols p{color:rgba(34,31,27,.82)}
.anote{margin-top:clamp(40px,6vh,64px);padding:clamp(24px,3vw,36px) clamp(24px,3.4vw,44px);
 border-left:2px solid var(--gold);background:rgba(255,255,255,.42)}
.anote p{font-family:var(--serif);font-style:italic;font-size:clamp(19px,1.8vw,25px);color:var(--forest);max-width:34em}
/* pillars strip */
.astrip{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(18px,2.6vw,34px);margin-top:clamp(44px,7vh,72px)}
.astrip div{padding-top:20px;border-top:1.5px solid rgba(34,31,27,.2)}
.astrip h3{font-family:var(--sans);font-weight:600;font-size:15px;letter-spacing:.02em;margin-bottom:9px;color:var(--forest)}
.astrip p{font-family:var(--sans);font-size:13.5px;line-height:1.75;color:rgba(34,31,27,.74)}
/* nearby */
.near{padding:clamp(70px,11vh,130px) 0;position:relative}
.near::before{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;
 background:linear-gradient(180deg,rgba(232,218,192,0),rgba(228,212,183,.62) 24%,rgba(228,212,183,.62) 76%,rgba(232,218,192,0))}
.near .wrap{position:relative;z-index:1}
.ngrid{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2.2vw,28px);margin-top:clamp(30px,5vh,46px)}
.ncard{position:relative;overflow:hidden;text-decoration:none;color:var(--cream);display:block;
 box-shadow:0 20px 44px -20px rgba(28,22,12,.5);transition:transform .5s var(--ease)}
.ncard:hover{transform:translateY(-5px)}
.ncard img{width:100%;aspect-ratio:4/3;object-fit:cover;filter:saturate(1.15) contrast(1.08)}
.ncard span{position:absolute;left:0;right:0;bottom:0;padding:32px 16px 14px;
 font-family:var(--sans);font-size:11px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;
 background:linear-gradient(180deg,transparent,rgba(15,32,24,.88))}
/* cta */
.acta{position:relative;color:var(--cream);padding:clamp(90px,14vh,160px) 0;overflow:hidden;text-align:center}
.acta::before{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;
 background:radial-gradient(ellipse 50% 42% at 50% 6%,rgba(196,164,104,.3),transparent 68%),
  linear-gradient(172deg,#12271C,#0F2018 55%,#16301F);
 -webkit-mask-image:linear-gradient(180deg,transparent,#000 9%,#000 100%);
 mask-image:linear-gradient(180deg,transparent,#000 9%,#000 100%)}
.acta .wrap{position:relative;z-index:1}
.acta h2{font-size:clamp(28px,3.4vw,48px);color:var(--cream);max-width:15em;margin:18px auto 30px}
.btn-gold{display:inline-block;text-decoration:none;color:var(--forest-deep);border:1px solid var(--gold);
 background:linear-gradient(135deg,var(--champagne-lt),var(--champagne) 45%,var(--gold));
 padding:19px 44px;font-family:var(--sans);font-size:11px;font-weight:600;letter-spacing:.3em;text-transform:uppercase;
 transition:filter .45s var(--ease),box-shadow .45s var(--ease)}
.btn-gold:hover{filter:brightness(1.07);box-shadow:0 6px 28px rgba(196,164,104,.35)}
footer{background:linear-gradient(180deg,#16301F,#0F2018);color:var(--cream);
 border-top:1px solid rgba(196,164,104,.35);padding:clamp(34px,6vh,52px) 0}
.foot{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap}
.foot .mark{color:var(--cream)}
.foot .mark small{color:var(--champagne)}
.foot .mark .mk{height:24px}
.foot-meta{font-family:var(--sans);font-size:10px;font-weight:600;letter-spacing:.26em;text-transform:uppercase;
 color:var(--champagne);opacity:.75}
.foot a{text-decoration:none;border-bottom:1px solid rgba(196,164,104,.5);padding-bottom:3px}
@media (max-width:1000px){.acols,.astrip,.ngrid{grid-template-columns:1fr}.astrip{gap:26px}.ngrid{gap:14px}}
@media (max-width:760px){
 body{font-size:16.5px;line-height:1.62}
 .wrap{padding:0 22px}
 .ahero .wrap{padding-top:118px}
 .ahero h1{font-size:clamp(30px,8.6vw,40px)}
 .alede{font-size:23px}
 .asec,.near{padding:66px 0}
 .acta{padding:80px 0}
 .acta h2{font-size:27px}
 .btn-gold{display:block;text-align:center;padding:20px 24px}
 .foot{flex-direction:column;align-items:flex-start;gap:14px}
}
@media (prefers-reduced-motion:reduce){*{transition-duration:.01ms!important}}
</style>'''
print("css ready")

# nav styles shared by every page (area pages get the whole header block)
NAVCSS = '''header{position:fixed;inset:0 0 auto 0;z-index:60;display:flex;justify-content:space-between;align-items:center;
 gap:24px;padding:22px clamp(24px,4.5vw,64px);transition:transform .45s var(--ease)}
header::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;opacity:0;
 transition:opacity .45s var(--ease);
 background:linear-gradient(180deg,rgba(250,246,238,.95),rgba(250,246,238,.74) 62%,rgba(250,246,238,0));
 -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
header.scrolled::before{opacity:1}
header.scrolled.on-dark::before{background:linear-gradient(180deg,rgba(15,32,24,.93),rgba(15,32,24,.68) 62%,rgba(15,32,24,0))}
header.tucked{transform:translateY(-104%)}
.mark{display:inline-flex;flex-direction:column;align-items:flex-start;gap:6px;text-decoration:none;
 color:var(--ink);transition:color .5s var(--ease);flex:0 0 auto}
.mark .mk{display:block;height:28px;width:auto;aspect-ratio:350/156;color:inherit;flex:0 0 auto}
.mark .mk use{fill:currentColor}
.mark small{font-family:var(--sans);font-size:7.5px;font-weight:600;letter-spacing:.3em;color:var(--taupe);
 transition:color .5s var(--ease)}
.nav{display:flex;gap:clamp(18px,2.4vw,38px);align-items:center;margin-left:auto;margin-right:clamp(18px,2.6vw,42px)}
.nav a{font-family:var(--sans);font-size:11px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;
 text-decoration:none;color:var(--forest);opacity:.78;padding:6px 0;position:relative;
 transition:opacity .35s var(--ease),color .5s var(--ease)}
.nav a::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:currentColor;
 transform:scaleX(0);transform-origin:left;transition:transform .4s var(--ease)}
.nav a:hover{opacity:1}
.nav a:hover::after,.nav a[aria-current="page"]::after{transform:scaleX(1)}
.nav a[aria-current="page"]{opacity:1}
.nav-cta{font-family:var(--sans);font-size:11px;font-weight:600;letter-spacing:.26em;text-transform:uppercase;
 text-decoration:none;color:var(--forest);padding-bottom:5px;border-bottom:1.5px solid var(--forest);flex:0 0 auto;
 transition:opacity .4s var(--ease),color .5s var(--ease),border-color .5s var(--ease)}
.nav-cta:hover{opacity:.55}
.nav-cta .short{display:none}
header.on-dark .mark{color:var(--cream)}
header.on-dark .mark small{color:var(--champagne)}
header.on-dark .nav a{color:var(--champagne)}
header.on-dark .nav-cta{color:var(--champagne);border-color:var(--gold)}
header.on-dark .menu-btn i{background:var(--champagne)}
/* mobile menu */
.menu-btn{display:none;flex-direction:column;justify-content:center;gap:5px;width:44px;height:44px;
 background:none;border:0;cursor:pointer;flex:0 0 auto;margin-left:auto}
.menu-btn i{display:block;width:22px;height:1.5px;background:var(--forest);transition:transform .4s var(--ease),opacity .3s}
body.menu-open .menu-btn i:nth-child(1){transform:translateY(6.5px) rotate(45deg)}
body.menu-open .menu-btn i:nth-child(2){opacity:0}
body.menu-open .menu-btn i:nth-child(3){transform:translateY(-6.5px) rotate(-45deg)}
body.menu-open .menu-btn i{background:var(--champagne)}
#menu{position:fixed;inset:0;z-index:55;display:flex;flex-direction:column;justify-content:center;
 padding:0 28px;opacity:0;visibility:hidden;transition:opacity .45s var(--ease),visibility .45s;
 background:radial-gradient(ellipse 60% 50% at 78% 14%,rgba(196,164,104,.26),transparent 66%),
  linear-gradient(168deg,#16301F,#0F2018 60%,#14291D)}
body.menu-open{overflow:hidden}
body.menu-open #menu{opacity:1;visibility:visible}
#menu a{font-family:var(--serif);font-style:italic;font-weight:300;font-size:clamp(30px,9vw,44px);
 color:var(--cream);text-decoration:none;padding:14px 0;border-bottom:1px solid rgba(196,164,104,.28);
 display:block;transform:translateY(14px);opacity:0;transition:transform .5s var(--ease),opacity .5s var(--ease)}
body.menu-open #menu a{transform:none;opacity:1}
#menu a:nth-child(2){transition-delay:.06s}
#menu a:nth-child(3){transition-delay:.12s}
#menu a:nth-child(4){transition-delay:.18s}
#menu a.m-cta{margin-top:26px;border-bottom:0;font-family:var(--sans);font-style:normal;font-weight:600;
 font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--forest-deep);text-align:center;
 background:linear-gradient(135deg,var(--champagne-lt),var(--champagne) 45%,var(--gold));
 border:1px solid var(--gold);padding:19px 24px}
@media (max-width:1100px){
 .nav{display:none}
 .nav-cta{display:none}
 .menu-btn{display:flex}
 header{padding:16px 20px}
 .mark .mk{height:24px}
}'''

# the smaller add-on injected into the three existing pages, which already style header/.mark/.nav-cta
NAVCSS_ADDON = NAVCSS[NAVCSS.index('.nav{display:flex'):]

def header_html(active=''):
    return '''<header class="on-dark">
  <a class="mark" href="/" aria-label="ONE Wellness — home"><svg class="mk" aria-hidden="true" focusable="false"><use href="#ow-mark"></use></svg><small>WELLNESS</small></a>
  <nav class="nav" aria-label="Primary">
      %s
  </nav>
  <a class="nav-cta" href="/#introduction"><span class="full">Request an introduction</span><span class="short">Enquire</span></a>
  <button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><i></i><i></i><i></i></button>
</header>

<div id="menu" role="dialog" aria-modal="true" aria-label="Menu">
  <a href="/">Home</a>
  %s
  <a class="m-cta" href="/#introduction">Request an introduction</a>
</div>''' % (nav_html(active),
             '\n  '.join('<a href="%s">%s</a>' % (h, l) for h, l in NAV_LINKS))

MENU_JS = '''  var btn = document.querySelector('.menu-btn');
  if (btn){
    btn.addEventListener('click', function(){
      var open = document.body.classList.toggle('menu-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    document.querySelectorAll('#menu a').forEach(function(a){
      a.addEventListener('click', function(){
        document.body.classList.remove('menu-open');
        btn.setAttribute('aria-expanded','false');
      });
    });
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && document.body.classList.contains('menu-open')) btn.click();
    });
  }'''
print("nav ready")

FOOT = '''<footer>
  <div class="wrap foot">
    <span class="mark" aria-hidden="true"><svg class="mk" aria-hidden="true" focusable="false"><use href="#ow-mark"></use></svg><small>WELLNESS</small></span>
    <span class="foot-meta"><a href="/areas">Areas we cover</a></span>
    <span class="foot-meta">© 2026 ONE Wellness</span>
  </div>
</footer>'''

HEADER_JS = '''<script>
(function(){
%s
  var hd = document.querySelector('header');
  var darks = document.querySelectorAll('.ahero, .acta, footer');
  var band = 58, lastY = 0, tuckable = window.matchMedia('(max-width:1100px)').matches;
  function update(){
    var y = window.scrollY, dark = false;
    darks.forEach(function(el){ var r = el.getBoundingClientRect(); if (r.top <= band && r.bottom >= 0) dark = true; });
    hd.classList.toggle('on-dark', dark);
    hd.classList.toggle('scrolled', y > 40);
    if (tuckable && !document.body.classList.contains('menu-open')){
      if (y > 160 && y > lastY + 4) hd.classList.add('tucked');
      else if (y < lastY - 4 || y < 120) hd.classList.remove('tucked');
    }
    lastY = y;
  }
  window.addEventListener('scroll', update, {passive:true});
  window.addEventListener('resize', update);
  update();
})();
</script>''' % MENU_JS

RAW = 'assets/archive/landmarks/'

def schema(d):
    return '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HealthAndBeautyBusiness","name":"ONE Wellness",
"description":"%s","url":"https://golden-oath-site.lovable.app/areas/%s",
"areaServed":{"@type":"Place","name":"%s, Riyadh","address":{"@type":"PostalAddress","addressLocality":"Riyadh","addressCountry":"SA"}},
"serviceType":"Private in-home personal training",
"founder":[{"@type":"Person","name":"Aaron Cook"},{"@type":"Person","name":"Bianca Cook"}]}
</script>''' % (d['meta'], d['slug'], d['name'])

def area_page(d, others):
    near = [o for o in others if o['slug'] != d['slug']][:3]
    ncards = '\n        '.join(
        '<a class="ncard" href="/areas/%s"><img src="%s%s" alt="%s, Riyadh" loading="lazy" decoding="async"><span>%s</span></a>'
        % (o['slug'], RAW, o['img'], o['name'], o['name']) for o in near)
    return '''%s
%s
%s
<div class="grain" aria-hidden="true"></div>
%s

<main>
  <section class="ahero">
    <img src="%s%s" alt="%s, Riyadh" fetchpriority="high" decoding="async">
    <div class="wrap">
      <span class="k">Areas we cover · Riyadh</span>
      <h1 class="display">Personal training at home in %s%s</h1>
      <p class="co">%s</p>
    </div>
  </section>

  <section class="asec">
    <div class="wrap">
      <p class="alede">%s</p>
      <div class="acols">
        <div><h2>The district</h2><p>%s</p></div>
        <div><h2>Training in your space</h2><p>%s</p></div>
      </div>
      <div class="anote"><p>%s</p></div>
      <div class="astrip">
        <div><h3>Training</h3><p>Sessions built around your body and your week — whether you trained yesterday or a decade ago.</p></div>
        <div><h3>Nutrition</h3><p>We build the nutrition around you, not the other way round — a plan you can actually stick to.</p></div>
        <div><h3>Daily habits</h3><p>Small routines — sleep, movement, recovery — that fit the life you already lead.</p></div>
      </div>
    </div>
  </section>

  <section class="near">
    <div class="wrap">
      <span class="k">Nearby</span>
      <div class="ngrid">
        %s
      </div>
    </div>
  </section>

  <section class="acta">
    <div class="wrap">
      <span class="k" style="color:var(--champagne)">%s</span>
      <h2 class="display">Coached by Olympic medallists, in your own home.</h2>
      <a class="btn-gold" href="/#introduction">Request an introduction</a>
    </div>
  </section>
</main>

%s
%s
''' % (head(d['title'], d['meta'], '/areas/' + d['slug']), CSS.replace('NAVCSS', NAVCSS), schema(d),
       SPRITE + '\n' + header_html('/areas'),
       RAW, d['img'], d['name'], d.get('article',''), d['name'], d['co'],
       d['lede'], d['character'], d['space'], d['note'], ncards, d['name'], FOOT, HEADER_JS)

for d in D:
    open(d['file'], 'w').write(area_page(d, D))
    print('wrote', d['file'], os.path.getsize(d['file']), 'bytes')

# ── /areas index ──
idx_cards = '\n        '.join(
 '''<a class="ncard" href="/areas/%s"><img src="%s%s" alt="%s, Riyadh" loading="lazy" decoding="async"><span>%s</span></a>'''
 % (d['slug'], RAW, d['img'], d['name'], d['name']) for d in D)

areas_index = '''%s
%s
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HealthAndBeautyBusiness","name":"ONE Wellness",
"description":"Private in-home personal training across Riyadh with Olympic medallists Aaron and Bianca Cook.",
"url":"https://golden-oath-site.lovable.app/areas","serviceType":"Private in-home personal training",
"areaServed":[%s]}
</script>
<div class="grain" aria-hidden="true"></div>
%s

<main>
  <section class="ahero">
    <img src="%sdiriyah.jpg" alt="Riyadh" fetchpriority="high" decoding="async">
    <div class="wrap">
      <span class="k">Areas we cover</span>
      <h1 class="display">We come to you, anywhere in Riyadh.</h1>
      <p class="co">Six districts · one city</p>
    </div>
  </section>

  <section class="asec">
    <div class="wrap">
      <p class="alede">There is no studio to travel to, so the only address that matters is yours.</p>
      <div class="ngrid" style="margin-top:clamp(40px,6vh,64px)">
        %s
      </div>
      <div class="anote" style="margin-top:clamp(44px,7vh,72px)"><p>Not on this list? We cover the whole city — tell us where you are at the introduction and we will tell you honestly whether we can do it justice.</p></div>
    </div>
  </section>

  <section class="acta">
    <div class="wrap">
      <span class="k" style="color:var(--champagne)">Riyadh</span>
      <h2 class="display">We are on a mission to make the people of Riyadh fitter, healthier and happier.</h2>
      <a class="btn-gold" href="/#introduction">Request an introduction</a>
    </div>
  </section>
</main>

%s
%s
''' % (head('Areas We Cover in Riyadh | ONE Wellness',
            'Private in-home personal training across Riyadh — Diriyah, the Diplomatic Quarter, Hittin, Al Malqa, Al Nakheel and Al Olaya.',
            '/areas'),
       CSS.replace('NAVCSS', NAVCSS),
       ','.join('{"@type":"Place","name":"%s, Riyadh"}' % d['name'] for d in D),
       SPRITE + '\n' + header_html('/areas'),
       RAW, idx_cards, FOOT, HEADER_JS)

open('areas.html','w').write(areas_index)
print('wrote areas.html', os.path.getsize('areas.html'), 'bytes')

# ── inject nav into the three existing pages ──
for f, active in (('index.html','/'), ('online.html','/online-coaching'), ('story.html','/story')):
    s = open(f).read()
    if 'class="nav"' in s:
        print(f, 'already has nav'); continue
    # replace the single-CTA header with the full nav header (keep each page's own on-dark default)
    s = re.sub(r'<header[^>]*>.*?</header>',
               lambda m: header_html(active) if 'menu-btn' not in m.group(0) else m.group(0),
               s, count=1, flags=re.S)
    # the pages already style header/.mark/.nav-cta; add only what is new
    s = s.replace('.nav-cta{font-family:var(--sans)', NAVCSS_ADDON + '\n.nav-cta{font-family:var(--sans)', 1)
    # menu script, before the page's own closing IIFE script
    s = s.replace('<script src="vendor/gsap.min.js"></script>',
                  '<script>\n(function(){\n%s\n})();\n</script>\n<script src="vendor/gsap.min.js"></script>' % MENU_JS, 1)
    open(f,'w').write(s)
    print(f, 'nav injected — nav:', s.count('class="nav"'), 'menu:', s.count('id="menu"'))
