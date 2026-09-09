# -*- coding: utf-8 -*-
"""Adds the SOP-required FAQ block plus FAQPage schema to online.html and story.html.
Questions are in the customer's words, answers match what the site actually promises."""
import re

FAQ_CSS = '''<style>
.faqsec{position:relative;padding:clamp(80px,12vh,140px) 0}
.faqsec::before{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;
 background:linear-gradient(180deg,rgba(232,218,192,0),rgba(228,212,183,.55) 22%,rgba(228,212,183,.55) 78%,rgba(232,218,192,0))}
.faqsec .wrap{position:relative;z-index:1}
.faqsec h2{font-size:clamp(28px,3.2vw,46px);color:var(--forest);margin:20px 0 0;max-width:14em}
.faq{max-width:52em;margin-top:clamp(34px,5vh,52px);border-top:1.5px solid rgba(34,31,27,.18)}
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
@media (max-width:760px){.faqsec{padding:70px 0}.faqsec h2{font-size:27px}.faq summary{font-size:19px}}
</style>'''

ONLINE = [
 ("Do I need a gym to do this?",
  "No. Your programme is written around whatever you have, whether that is a full gym, a set of dumbbells at home, or nothing but the floor. Tell us what you have access to at the start and we build from there."),
 ("How is this different from an app or a training plan I could download?",
  "An app gives everybody the same programme. This is written for you by Aaron or Bianca, adjusted every block as you progress, and you send your lifts in so they can correct your technique. You are talking to a person, not a piece of software."),
 ("How often do I actually speak to my coach?",
  "You have direct messaging with Aaron or Bianca throughout, plus a scheduled video call each month to review what is working and change what is not. You are not left on your own between calls."),
 ("I travel a lot for work. Does that break the programme?",
  "It is designed to survive travel. Tell us your schedule and the programme bends around it, including hotel gym sessions and weeks where the plan has to be simpler. A programme you abandon the moment life gets busy is worth nothing."),
 ("Can I choose Aaron or Bianca?",
  "Yes. You pick when you join, or you can leave it to them and they will match you to whoever fits your goal best."),
 ("What if I have never trained properly before?",
  "That describes most of the people we work with. Nobody is asking you to train like an Olympian. The first block is about building something you can repeat, not proving anything."),
]

STORY = [
 ("Do Aaron and Bianca coach every session themselves?",
  "Yes. This is not an agency that sends whoever is available. They coach personally, which is why the client list is deliberately short."),
 ("Do I need to be an athlete to train with them?",
  "No. Most of the people they coach have not trained seriously in years, and several never have. Two decades at the top of world sport is what shapes the method, not the standard expected of you."),
 ("Are they still competing?",
  "No. Aaron moved into coaching and was Head Taekwondo Coach at Mahd Sports Academy in Riyadh from 2022. Their competitive careers are behind them and coaching is the work now."),
 ("Where are they based?",
  "Riyadh. In-home private coaching is across the city, and one to one online coaching is available anywhere in the world."),
 ("What does an Olympic background actually change about the coaching?",
  "Patience, precision and perspective. Programmes are built in blocks and judged over months, technique is corrected by someone who spent twenty years being corrected, and they know you do not need to train at the limit to get results."),
]

def block(kicker, heading, items):
    rows = '\n        '.join(
        '<details><summary>%s</summary><div class="a">%s</div></details>' % (q, a) for q, a in items)
    schema = ('<script type="application/ld+json">\n'
              '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}\n'
              '</script>') % ','.join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
        % (q.replace('"', '\\"'), a.replace('"', '\\"')) for q, a in items)
    html = '''
  <!-- FAQ -->
  <section class="faqsec">
    <div class="wrap">
      <span class="k">%s</span>
      <h2 class="display" data-words>%s</h2>
      <div class="faq">
        %s
      </div>
    </div>
  </section>
''' % (kicker, heading, rows)
    return html, schema

for f, kicker, heading, items in [
        ('online.html', 'Questions', 'The things people ask before they join.', ONLINE),
        ('story.html',  'Questions', 'What people ask about Aaron and Bianca.',  STORY)]:
    s = open(f).read()
    if 'faqsec' in s:
        print(f, 'already has one'); continue
    html, schema = block(kicker, heading, items)
    s = s.replace('</style>', '</style>\n' + FAQ_CSS, 1)          # styles
    s = s.replace('<link rel="canonical"', schema + '\n<link rel="canonical"', 1)  # FAQPage schema
    s = s.replace('</main>', html + '\n</main>', 1)               # the block itself, last section
    open(f, 'w').write(s)
    print('%s  questions=%d  FAQPage=%d' % (f, len(items), s.count('FAQPage')))
