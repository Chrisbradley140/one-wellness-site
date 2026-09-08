# -*- coding: utf-8 -*-
"""Privacy policy, required before the Meta pixel and the GHL form go live."""
import importlib.util, contextlib, io, os
spec = importlib.util.spec_from_file_location('ba', 'build-areas.py')
ba = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(ba)

CSS = ba.CSS.replace('NAVCSS', ba.NAVCSS)

EXTRA = '''<style>
.legal{padding:clamp(150px,20vh,220px) 0 clamp(80px,12vh,140px)}
.legal .k{display:block;margin-bottom:18px}
.legal h1{font-size:clamp(38px,4.6vw,64px);color:var(--forest);margin-bottom:16px}
.legal .upd{font-family:var(--sans);font-size:12px;letter-spacing:.16em;text-transform:uppercase;
 color:var(--taupe);margin-bottom:clamp(40px,6vh,64px)}
.legal .body{max-width:44em}
.legal h2{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(24px,2.3vw,32px);
 color:var(--forest);margin:clamp(38px,5vh,54px) 0 14px}
.legal p{color:rgba(34,31,27,.82);margin-bottom:14px;font-size:18px}
.legal ul{margin:0 0 14px 22px}
.legal li{color:rgba(34,31,27,.82);margin-bottom:9px;font-size:18px}
.legal a{color:var(--forest);text-decoration:underline;text-underline-offset:3px}
@media (max-width:760px){.legal{padding:120px 0 76px}.legal h1{font-size:32px}.legal p,.legal li{font-size:16.5px}}
</style>'''

BODY = '''
  <section class="legal">
    <div class="wrap">
      <span class="k">Legal</span>
      <h1 class="display">Privacy policy</h1>
      <p class="upd">Last updated 7 September 2026</p>
      <div class="body">
        <p>ONE Wellness provides private in-home personal training in Riyadh, Saudi Arabia, and
          one-to-one online coaching worldwide. This policy explains what we collect when you use this
          website, why we collect it, and what we do with it.</p>

        <h2>What we collect</h2>
        <p>When you send an enquiry we collect the details you type into the form: your name, your phone
          number or email address, and anything you tell us about what you want to achieve. On the online
          coaching page we also collect the country or city you are in and which coach you would prefer.</p>
        <p>We do not ask for payment details on this website, and we never ask for them by email.</p>
        <p>Like most websites we also receive standard technical information automatically, including your
          approximate location, browser and device type, and which pages you looked at.</p>

        <h2>Why we collect it</h2>
        <ul>
          <li>To reply to your enquiry and arrange an introduction</li>
          <li>To manage your coaching if you become a client</li>
          <li>To understand which parts of the site are useful, so we can improve them</li>
        </ul>
        <p>We do not sell your information, and we do not share it with anyone who is not directly involved
          in providing your coaching.</p>

        <h2>How long we keep it</h2>
        <p>If you enquire and do not become a client, we keep your details for up to twelve months and then
          delete them. If you become a client, we keep your records for as long as we coach you and for a
          reasonable period afterwards.</p>

        <h2>Cookies and tracking</h2>
        <p>This site uses analytics to count visits and see which pages people read. It may also use a
          Meta (Facebook and Instagram) pixel so we can measure whether our advertising is working. These
          set cookies in your browser. You can block or delete cookies in your browser settings at any
          time, and the site will still work.</p>

        <h2>Discretion</h2>
        <p>Discretion matters to our clients and it matters to us. We do not publish client names, we do
          not photograph anyone's home, and we do not post about who we coach. That applies to this
          website and to everything else we do.</p>

        <h2>Your choices</h2>
        <p>You can ask us what information we hold about you, ask us to correct it, or ask us to delete it.
          Contact us using the enquiry form on this site and we will action it.</p>

        <h2>Contact</h2>
        <p>Questions about this policy can be sent through the <a href="/#introduction">enquiry form</a>.
          Aaron or Bianca will reply personally.</p>
      </div>
    </div>
  </section>
'''

page = '''%s
%s
%s
<div class="grain" aria-hidden="true"></div>
%s

<main>%s</main>

%s
%s
''' % (ba.head('Privacy Policy | ONE Wellness',
               'How ONE Wellness collects, uses and protects your information when you use this website or enquire about coaching.',
               '/privacy'),
       CSS, EXTRA, ba.SPRITE + '\n' + ba.header_html(''), BODY, ba.FOOT, ba.HEADER_JS)

# this page has no photo hero, so the header should only invert over the footer
page = page.replace(".ahero, .acta, footer", "footer")
open('privacy.html','w').write(page)
print('wrote privacy.html', os.path.getsize('privacy.html'), 'bytes')
