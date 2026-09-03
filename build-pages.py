# -*- coding: utf-8 -*-
"""Rebuilds /about and /private-coaching on the current brand system.
Reuses the shared head/CSS/nav/footer from build-areas.py so every page stays identical."""
import re, os, importlib.util
spec = importlib.util.spec_from_file_location('ba', 'build-areas.py')
ba = importlib.util.module_from_spec(spec)
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(ba)

CSS   = ba.CSS.replace('NAVCSS', ba.NAVCSS)
HEAD  = ba.head
SPRITE= ba.SPRITE
FOOT  = ba.FOOT
RAW   = 'assets/archive/'

def header(active): return ba.header_html(active)

# page-specific styles layered on the shared sheet
EXTRA = '''<style>
.plede{font-family:var(--serif);font-style:italic;font-weight:300;font-size:clamp(25px,3vw,42px);
 color:var(--forest);max-width:20em;line-height:1.24}
.steps{margin-top:clamp(44px,7vh,72px);border-top:1.5px solid rgba(34,31,27,.18)}
.step{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,8fr);gap:clamp(20px,3.4vw,60px);
 align-items:baseline;padding:clamp(24px,3.4vh,36px) 0;border-bottom:1px solid rgba(34,31,27,.15)}
.step b{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(24px,2.3vw,34px);color:var(--forest)}
.step p{color:rgba(34,31,27,.8);max-width:32em}
.step p+p{margin-top:10px}
.incl3{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(18px,2.4vw,32px);margin-top:clamp(40px,6vh,64px)}
.icard{position:relative;overflow:hidden;isolation:isolate;color:var(--cream);
 padding:clamp(26px,3vw,38px) clamp(22px,2.4vw,30px) clamp(30px,3.4vw,42px);
 box-shadow:0 20px 44px -18px rgba(15,32,24,.5)}
.icard::before{content:"";position:absolute;inset:0;z-index:-1;
 background:radial-gradient(ellipse 70% 60% at 78% 12%,rgba(196,164,104,.28),transparent 62%),
  linear-gradient(158deg,#1E4030,#16301F 46%,#0F2018)}
.icard::after{content:"";position:absolute;left:0;top:0;height:2px;width:100%;
 background:linear-gradient(90deg,var(--gold),rgba(196,164,104,0))}
.icard h3{font-family:var(--serif);font-style:italic;font-weight:300;font-size:clamp(24px,2.3vw,32px);
 color:var(--champagne);margin-bottom:12px}
.icard p{font-family:var(--sans);font-size:14px;line-height:1.78;color:rgba(247,243,236,.8)}
.faq{max-width:52em;margin-top:clamp(38px,6vh,58px);border-top:1.5px solid rgba(34,31,27,.18)}
.faq details{border-bottom:1px solid rgba(34,31,27,.15)}
.faq summary{list-style:none;cursor:pointer;padding:clamp(20px,2.6vh,26px) 44px clamp(20px,2.6vh,26px) 0;
 font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(20px,1.9vw,26px);color:var(--forest);
 position:relative;transition:opacity .3s var(--ease)}
.faq summary::-webkit-details-marker{display:none}
.faq summary:hover{opacity:.66}
.faq summary::after{content:"";position:absolute;right:8px;top:50%;width:11px;height:11px;
 border-right:1.5px solid var(--taupe);border-bottom:1.5px solid var(--taupe);
 transform:translateY(-70%) rotate(45deg);transition:transform .35s var(--ease)}
.faq details[open] summary::after{transform:translateY(-30%) rotate(-135deg)}
.faq .a{padding:0 0 clamp(22px,3vh,30px);font-family:var(--sans);font-size:14.5px;line-height:1.8;
 color:rgba(34,31,27,.78);max-width:44em}
.tenets{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(22px,3.4vw,52px);margin-top:clamp(44px,7vh,72px)}
.tenets div{padding-top:22px;border-top:1.5px solid rgba(34,31,27,.2)}
.tenets h3{font-family:var(--serif);font-style:italic;font-weight:300;font-size:clamp(26px,2.5vw,36px);
 color:var(--forest);margin-bottom:12px}
.tenets p{font-family:var(--sans);font-size:14px;line-height:1.78;color:rgba(34,31,27,.76)}
.thero{position:relative;min-height:80vh;display:flex;align-items:center;background:var(--forest-deep);overflow:hidden}
.thero::before{content:"";position:absolute;inset:0;z-index:0;
 background:radial-gradient(ellipse 55% 50% at 76% 26%,rgba(196,164,104,.3),transparent 66%),
  radial-gradient(ellipse 70% 55% at 8% 82%,rgba(168,135,86,.22),transparent 68%),
  linear-gradient(162deg,#16301F,#0F2018 54%,#14291D)}
.thero .wrap{position:relative;z-index:2;padding-top:150px;padding-bottom:clamp(50px,8vh,90px)}
.thero .k{display:block;margin-bottom:20px;color:var(--champagne)}
.thero h1{font-size:clamp(38px,5.4vw,80px);color:var(--cream);max-width:12em}
.thero p{margin-top:26px;font-family:var(--sans);font-size:14px;line-height:1.85;letter-spacing:.03em;
 color:rgba(247,243,236,.78);max-width:36em}
.founders{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:clamp(32px,5vw,76px);
 align-items:center;margin-top:clamp(44px,7vh,72px)}
.founders figure{overflow:hidden;box-shadow:0 30px 60px -24px rgba(28,22,12,.5)}
.founders img{width:100%;aspect-ratio:4/3;object-fit:cover;filter:saturate(1.1) contrast(1.05)}
.founders h2{font-family:var(--serif);font-style:italic;font-weight:300;font-size:clamp(28px,3vw,42px);
 color:var(--forest);margin-bottom:16px}
.founders p{color:rgba(34,31,27,.82);max-width:30em}
.founders a.more{display:inline-block;margin-top:22px;font-family:var(--sans);font-size:11px;font-weight:600;
 letter-spacing:.26em;text-transform:uppercase;color:var(--forest);text-decoration:none;
 border-bottom:1.5px solid var(--forest);padding-bottom:5px;transition:opacity .4s var(--ease)}
.founders a.more:hover{opacity:.6}
@media (max-width:1000px){.incl3,.tenets,.founders{grid-template-columns:1fr}.step{grid-template-columns:1fr;gap:8px}}
@media (max-width:760px){.plede{font-size:24px}.thero h1{font-size:clamp(31px,8.8vw,42px)}
 .thero .wrap{padding-top:120px}.faq summary{font-size:19px}}
</style>'''
print('shared loaded')

FAQ = [
 ("Do I need a home gym?",
  "No. We have coached people in a spare room, a garage, a garden and a full basement gym, and the programme is written for whatever you actually have. Where kit is genuinely needed we bring it with us, and if you would rather train at a gym of your choice, we can do that instead."),
 ("How long is a session, and how often?",
  "Sessions are typically an hour. Most clients train two or three times a week — enough to progress properly without taking over your calendar. The schedule is set around your week, not ours."),
 ("Who actually coaches me?",
  "Aaron or Bianca, in person. This is not an agency that sends whoever is free — that is the whole point of keeping the client list short."),
 ("I have not trained seriously in years. Is this for me?",
  "Yes, and it is most of who we work with. Nobody is asking you to train like an Olympian. The first block is about building something you can repeat, not about proving anything."),
 ("How private is it?",
  "Completely. No client names, no photographs, no social posts, and no mention of who else we coach — including to you. Discretion works in both directions."),
 ("What happens at the introduction?",
  "A conversation, not a sales call. We talk about what you want, look at your space, and tell you honestly whether we are the right fit. If we are not, we will say so."),
]

def faq_schema(items):
    qs = ','.join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
                  % (q.replace('"','\\"'), a.replace('"','\\"')) for q, a in items)
    return '<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}\n</script>' % qs

faq_html = '\n        '.join(
 '<details><summary>%s</summary><div class="a">%s</div></details>' % (q, a) for q, a in FAQ)

PRIVATE = '''%s
%s
%s
%s
<div class="grain" aria-hidden="true"></div>
%s

<main>
  <section class="ahero">
    <img src="%sriyadh-session.jpg" alt="A private coaching session on a Riyadh terrace" fetchpriority="high" decoding="async">
    <div class="wrap">
      <span class="k">Private coaching · Riyadh</span>
      <h1 class="display">One-to-one coaching, in your own space.</h1>
      <p class="co">By introduction · A short client list</p>
    </div>
  </section>

  <section class="asec">
    <div class="wrap">
      <p class="plede">We do not have a studio. We have a small number of clients, and we come to them.</p>

      <div class="steps">
        <div class="step"><b>The session</b>
          <p>An hour, in your home or a gym of your choice, coached in person by Aaron or Bianca. Warm-up, the work that matters that day, and a proper finish — not a circuit designed to make you sweat for the sake of it.</p>
          <p>Every session is written before we arrive and adjusted while we are there, because the plan on paper is not always the plan your body agrees to.</p></div>
        <div class="step"><b>Your space</b>
          <p>A spare room, a garage, a garden, a home gym — or a gym of your choice. We look at what you already have before suggesting you buy anything, and we travel with whatever the room is missing.</p></div>
        <div class="step"><b>Your schedule</b>
          <p>Two or three sessions a week suits most people. Times are set around your week and moved when your week moves — a programme you abandon in a fortnight is worth nothing.</p></div>
        <div class="step"><b>Between sessions</b>
          <p>Nutrition built around your household and your travel, and the daily habits — sleep, steps, recovery — that decide whether the training holds. Direct access to your coach when something changes.</p></div>
      </div>

      <div class="incl3">
        <div class="icard"><h3>Training</h3><p>Sessions built around your body and your week — whether you trained yesterday or a decade ago.</p></div>
        <div class="icard"><h3>Nutrition</h3><p>We build the nutrition around you, not the other way round — a plan you can actually stick to.</p></div>
        <div class="icard"><h3>Daily habits</h3><p>Small routines — sleep, movement, recovery — that fit the life you already lead. Nobody is asking you to train like an Olympian.</p></div>
      </div>
    </div>
  </section>

  <section class="near">
    <div class="wrap">
      <span class="k">The first ninety days</span>
      <div class="steps" style="margin-top:clamp(30px,5vh,48px)">
        <div class="step"><b>Weeks 1–4</b><p>Establishing a baseline and building the habit of turning up. Load is deliberately conservative — we are finding out how you move and how you recover before we ask anything of you.</p></div>
        <div class="step"><b>Weeks 5–8</b><p>The work gets real. Progressive loading, technique refined session by session, nutrition adjusted around what has actually been happening rather than what was planned.</p></div>
        <div class="step"><b>Weeks 9–12</b><p>The first honest review. What has changed, what has not, and what the next block should look like. This is where most people notice the difference outside the session — sleep, energy, how they carry themselves.</p></div>
      </div>
    </div>
  </section>

  <section class="asec">
    <div class="wrap">
      <span class="k">Questions</span>
      <div class="faq">
        %s
      </div>
    </div>
  </section>

  <section class="acta">
    <div class="wrap">
      <span class="k" style="color:var(--champagne)">Private coaching</span>
      <h2 class="display">We keep the list short on purpose.</h2>
      <a class="btn-gold" href="/#introduction">Request an introduction</a>
    </div>
  </section>
</main>

%s
%s
''' % (HEAD('Private Personal Training in Riyadh | ONE Wellness',
            'One-to-one private personal training in your own home in Riyadh, coached in person by Olympic medallists Aaron and Bianca Cook.',
            '/private-coaching'),
       CSS, EXTRA, faq_schema(FAQ),
       SPRITE + '\n' + header(''),
       RAW, faq_html, FOOT, ba.HEADER_JS)

open('private.html','w').write(PRIVATE)
print('wrote private.html', os.path.getsize('private.html'), 'bytes')

ABOUT = '''%s
%s
%s
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"AboutPage","name":"About ONE Wellness",
"mainEntity":{"@type":"HealthAndBeautyBusiness","name":"ONE Wellness",
"description":"Private in-home personal training in Riyadh, coached by Olympic medallists Aaron and Bianca Cook.",
"areaServed":{"@type":"City","name":"Riyadh","address":{"@type":"PostalAddress","addressCountry":"SA"}},
"founder":[{"@type":"Person","name":"Aaron Cook"},{"@type":"Person","name":"Bianca Cook"}]}}
</script>
<div class="grain" aria-hidden="true"></div>
%s

<main>
  <section class="thero">
    <div class="wrap">
      <span class="k">About</span>
      <h1 class="display">A very small practice, run to a very high standard.</h1>
      <p>ONE Wellness is private in-home coaching in Riyadh. No studio, no membership, no class timetable —
        two coaches who spent their careers at the top of world sport, working with a deliberately short list
        of clients in their own homes.</p>
    </div>
  </section>

  <section class="asec">
    <div class="wrap">
      <p class="plede">Most coaching fails for boring reasons: the gym is too far, the plan is too rigid, and nobody notices when you stop.</p>
      <div class="acols">
        <div><h2>What we do differently</h2><p>We remove the friction that ends most programmes. The session comes to you, at a time that fits your week, written for the space and equipment you actually have. And because the list is short, we notice immediately when something slips.</p></div>
        <div><h2>What we are not</h2><p>We are not an agency with a roster of trainers, and we are not a transformation programme with a countdown on it. If you want to be shouted at for six weeks and then left alone, we are the wrong choice — and we will tell you so at the introduction.</p></div>
      </div>

      <div class="tenets">
        <div><h3>Discretion</h3><p>No client names, no photographs, no social posts — including about you, and including to you about anyone else. It works in both directions or it is not discretion.</p></div>
        <div><h3>Patience</h3><p>Nobody peaks in six weeks. Programmes are built in blocks and judged over months, which is exactly why they hold when life gets busy.</p></div>
        <div><h3>Honesty</h3><p>If we are not the right fit, we say so at the introduction rather than taking the work. If something is not progressing, you hear it from us first.</p></div>
      </div>
    </div>
  </section>

  <section class="near">
    <div class="wrap">
      <span class="k">Who we work with</span>
      <div class="steps" style="margin-top:clamp(28px,4.5vh,44px)">
        <div class="step"><b>Beginners</b><p>Most of our clients have not trained seriously in years, and several never have. Nobody is asking you to train like an Olympian — the first block is about building something you can repeat.</p></div>
        <div class="step"><b>The time-poor</b><p>Executives, founders and parents whose calendars move without warning. The programme is designed to bend rather than break when your week changes.</p></div>
        <div class="step"><b>The private</b><p>People who would simply rather not train in public. That is a perfectly good reason, and it is the reason this service exists.</p></div>
      </div>
    </div>
  </section>

  <section class="asec">
    <div class="wrap">
      <div class="founders">
        <figure><img src="%sfounders-portrait.jpg" alt="Aaron and Bianca Cook" loading="lazy" decoding="async"></figure>
        <div>
          <h2>Aaron &amp; Bianca Cook</h2>
          <p>More than two decades at the very top of world taekwondo between them — Olympic medals, world
            titles and world No.1 rankings — and now a practice in Riyadh built on the method underneath all of it
            rather than the medals themselves.</p>
          <p>They coach every session personally.</p>
          <a class="more" href="/story">Read their story</a>
        </div>
      </div>
    </div>
  </section>

  <section class="acta">
    <div class="wrap">
      <span class="k" style="color:var(--champagne)">ONE Wellness</span>
      <h2 class="display">We are on a mission to make the people of Riyadh fitter, healthier and happier.</h2>
      <a class="btn-gold" href="/#introduction">Request an introduction</a>
    </div>
  </section>
</main>

%s
%s
''' % (HEAD('About ONE Wellness | Private Coaching in Riyadh',
            'ONE Wellness is a private in-home coaching practice in Riyadh, run by Olympic medallists Aaron and Bianca Cook for a deliberately short list of clients.',
            '/about'),
       CSS, EXTRA,
       SPRITE + '\n' + header(''),
       RAW, FOOT, ba.HEADER_JS)

# the about hero is typographic, not a photo — teach the header which sections are dark
ABOUT = ABOUT.replace(".ahero, .acta, footer", ".thero, .acta, footer")
open('about.html','w').write(ABOUT)
print('wrote about.html', os.path.getsize('about.html'), 'bytes')
