from pybtex.database.input import bibtex
import json
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from html import escape

def load_people_data():
    with open('people.json', 'r') as f:
        return json.load(f)

_people_data = load_people_data()

def friends():
    friend_list = [
        (p['name'], p['url'], p.get('institution', ''))
        for p in _people_data['people'] if p.get('show_in_list')
    ]
    return sorted(friend_list, key=lambda x: x[0].split()[-1])

def gen_friend_list_html():
    return ''.join(
        f'<li><a href="{escape(link, quote=True)}" target="_blank">{escape(name)}</a>'
        f'<span>{escape(school)}</span></li>'
        for name, link, school in friends()
    )

# Interactive lambda-calculus email reveal. Kept as a plain (non-f) string so
# the CSS/JS braces stay literal; it is spliced into the bio f-string verbatim.
EMAIL_REDUCER = """
<div id="lambda-mail" class="lambda-mail" aria-live="polite">
  <div class="lambda-term" id="lambda-term"></div>
  <div class="lambda-controls">
    <button type="button" class="btn btn-sm btn-outline-secondary lambda-btn" id="lambda-prev">&larr; Prev</button>
    <button type="button" class="btn btn-sm btn-primary lambda-btn" id="lambda-next">↳ &beta;-reduce</button>
    <button type="button" class="btn btn-sm btn-link lambda-btn" id="lambda-reset">Reset</button>
    <button type="button" class="btn btn-sm btn-outline-secondary lambda-btn" id="lambda-copy" style="display: none;"> Copy email</button>
  </div>
  <div class="lambda-hint" id="lambda-hint">Don't see it? Try running it.</div>
</div>
<style>
.lambda-mail { margin-top: 0.5rem; }
.lambda-term {
  font-family: 'SFMono-Regular', Consolas, Menlo, monospace;
  font-size: 1.05rem;
  padding: 0.6rem 0.8rem;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  display: inline-block;
  white-space: nowrap;
  overflow-x: auto;
  max-width: 100%;
}
.lambda-term .lam { color: #6f42c1; font-weight: 700; }
.lambda-term .a1 { color: #c0392b; }
.lambda-term .a2 { color: #2980b9; }
.lambda-term .a3 { color: #1e8449; }
.lambda-term .just-subst {
  background: #fff3cd;
  border-radius: 3px;
  padding: 0 2px;
  animation: lambdaFlash 0.7s ease;
}
@keyframes lambdaFlash {
  from { background: #ffe08a; }
  to { background: #fff3cd; }
}
.lambda-term a.email-link { text-decoration: none; color: inherit; }
.lambda-term a.email-link:hover { text-decoration: underline; }
.lambda-controls { margin-top: 0.5rem; display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap; }
.lambda-hint { margin-top: 0.35rem; font-size: 0.85rem; color: #6c757d; font-style: italic; }
.lambda-mail .lambda-btn:disabled { opacity: 0.45; cursor: default; }
</style>
<script>
(function () {
  var termEl = document.getElementById('lambda-term');
  var prevBtn = document.getElementById('lambda-prev');
  var nextBtn = document.getElementById('lambda-next');
  var resetBtn = document.getElementById('lambda-reset');
  var copyBtn = document.getElementById('lambda-copy');
  var hintEl = document.getElementById('lambda-hint');
  if (!termEl || !nextBtn) return;

  var L = '<span class="lam">λ</span>';
  // Each step is the term after one β-reduction; the newly substituted
  // argument carries .just-subst so you can see what got plugged in.
  var steps = [
    '(' + L + '<span class="a1">x</span>.' + L + '<span class="a2">y</span>.' + L + '<span class="a3">z</span>. <span class="a3">z</span>@<span class="a1">x</span>.<span class="a2">y</span>) <span class="a1">princeton</span> <span class="a2">edu</span> <span class="a3">mikehe</span>',
    '(' + L + '<span class="a2">y</span>.' + L + '<span class="a3">z</span>. <span class="a3">z</span>@<span class="a1 just-subst">princeton</span>.<span class="a2">y</span>) <span class="a2">edu</span> <span class="a3">mikehe</span>',
    '(' + L + '<span class="a3">z</span>. <span class="a3">z</span>@<span class="a1">princeton</span>.<span class="a2 just-subst">edu</span>) <span class="a3">mikehe</span>',
    '<span class="a3 just-subst">mikehe</span>@<span class="a1">princeton</span>.<span class="a2">edu</span>'
  ];
  // Address kept as char codes so no plaintext / mailto: string ever appears in
  // the page source for email harvesters to scrape. Assembled only on click.
  var enc = [109,105,107,101,104,101,64,112,114,105,110,99,101,116,111,110,46,101,100,117];
  function decode() {
    var s = '';
    for (var k = 0; k < enc.length; k++) { s += String.fromCharCode(enc[k]); }
    return s;
  }

  // Clipboard copy with a graceful fallback for browsers without the async API.
  function copyEmail() {
    var addr = decode();
    function done() {
      var old = copyBtn.innerHTML;
      copyBtn.innerHTML = '✓ Copied';
      setTimeout(function () { copyBtn.innerHTML = old; }, 1500);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(addr).then(done, function () { legacyCopy(addr); done(); });
    } else {
      legacyCopy(addr);
      done();
    }
  }
  function legacyCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'absolute';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
  }
  if (copyBtn) copyBtn.addEventListener('click', copyEmail);

  var i = 0;

  function render() {
    var atFinal = (i === steps.length - 1);
    if (atFinal) {
      // href starts as "#" so no mailto: appears in the source. It is filled in
      // with the real address on the first genuine user interaction (hover /
      // focus / touch / right-click), which restores native left/middle-click,
      // drag, and "Copy Link Address" while keeping crawlers out.
      termEl.innerHTML = '<a class="email-link" href="#" id="lambda-email-link" role="button">' + steps[i] + '</a>';
      var link = document.getElementById('lambda-email-link');
      if (link) {
        var armed = false;
        function arm() {
          if (armed) return;
          armed = true;
          link.setAttribute('href', 'mailto:' + decode());
        }
        ['mouseenter', 'focus', 'touchstart', 'pointerdown', 'contextmenu'].forEach(function (ev) {
          link.addEventListener(ev, arm);
        });
        // If activation somehow beats arming, navigate explicitly.
        link.addEventListener('click', function (e) {
          if (!armed) { e.preventDefault(); arm(); window.location.href = 'mailto:' + decode(); }
        });
      }
      nextBtn.innerHTML = 'normal form ✓';
      hintEl.innerHTML = '🎉 There it is — click the address to email me, or copy it.';
    } else {
      termEl.innerHTML = steps[i];
      nextBtn.innerHTML = '↳ β-reduce';
      hintEl.innerHTML = "Don't see it? Try running it.";
    }
    prevBtn.disabled = (i === 0);
    nextBtn.disabled = atFinal;
    if (copyBtn) copyBtn.style.display = atFinal ? '' : 'none';
  }

  nextBtn.addEventListener('click', function () { if (i < steps.length - 1) { i++; render(); } });
  prevBtn.addEventListener('click', function () { if (i > 0) { i--; render(); } });
  resetBtn.addEventListener('click', function () { i = 0; render(); });
  render();
})();
</script>
"""

def get_personal_data():
    name = ["Mike", "He"]
    bio_text = f"""
<p>
                    I am a Ph.D. student at the <a href="https://pl.cs.princeton.edu/" target="_blank">Princeton Programming Languages Group</a> advised by Prof. <a href="https://www.cs.princeton.edu/~aartig/" target="_blank"> Aarti Gupta</a>.
                    I am broadly interested in programming languages, formal methods and compilers.
                    My current research focuses on practical formal and semi-formal methods for distributed systems and agentic systems, and I am working with the <a href="https://p-org.github.io/P" target="_blank">P ecosystem</a> for verifying and reasoning about distributed systems.
                </p>
<p>Before joining Princeton, I studied at the <a href="https://cs.washington.edu" target="_blank">University of Washington</a>, where I was privileged to work with Prof. <a href="https://ztatlock.net/" target="_blank">Zachary Tatlock</a> on equality saturation and its applications to machine learning compilers.
                </p>
<p>In my free time, I enjoy playing the violin (I've been playing it longer than coding). You can find my archived recordings <a href="recordings.html">here</a>.</p>
    <div class="contact-links" aria-label="Contact and profiles">
        <a class="cv-link" href="assets/cv.pdf" target="_blank">Curriculum vitae <span aria-hidden="true">↗</span></a>
        <a href="https://scholar.google.com/citations?hl=en&user=dhtWqm8AAAAJ&view_op=list_works&sortby=pubdate" target="_blank">Scholar</a>
        <a href="https://github.com/AD1024" target="_blank">GitHub</a>
        <a href="https://twitter.com/1SHL10" target="_blank">Twitter</a>
        <a href="https://www.linkedin.com/in/deyuan-mike-he" target="_blank">LinkedIn</a>
    </div>
    <div class="bio-disclosures">
        <details class="email-disclosure"><summary>λ-Mail</summary>{EMAIL_REDUCER}</details>
        <details class="awards-disclosure"><summary>Awards &amp; honors</summary><ul>
<li>2022: <a href="https://news.cs.washington.edu/2022/02/22/allen-school-undergraduates-recognized-by-the-computing-research-association-for-advancing-health-sensing-programming-languages-and-systems-research/" target="_blank">CRA Outstanding Undergraduate Researcher Award, Honorable Mention</a></li>
<li>2020: Lynn Conway Research Award (DTR Team)</li>
<li>2019: JASSO Scholarship, Waseda University</li>
<li>2018 → 2022: Annual Dean's List, University of Washington</li>
<li>2016: NOIp 2nd Prize, Beijing Regional</li>
</ul></details>
    </div>
    """
    footer = f"""
    <section class="site-section personal-section" aria-labelledby="beyond-research">
        <div class="section-heading"><h2 id="beyond-research">Beyond research</h2><a class="text-link" href="recordings.html">Violin recordings <span aria-hidden="true">↗</span></a></div>
        <div class="personal-intro"><p>Classical music, the violin, and a few other things.</p></div>
        <details class="personal-details"><summary>A little more about me</summary><ul>
<li>I love classical music and enjoy playing the violin. I've been playing the violin for about 20 years.
                     I received the Lv.9 certification issued by the Central Conservatory of Music when I was in middle school.
                    You can find some of my recordings <a href="recordings.html">here</a>.
                    Some video recordings are available @ <a href="https://space.bilibili.com/11936677" target="_blank">Bilibili</a> (the website is in Chinese).</li>
<li>I was a part-time translator / proofreading editor in <a href="https://www.youtube.com/channel/UCoSrY_IQQVpmIRZ9Xf-y93g" target="_blank">Gawr Gura</a>'s Chinese fansub team. Gura, now graduated, was a virtual streamer at YouTube affiliated with <a href="https://en.hololive.tv/member" target="_blank">Hololive Production</a>.</li>
<li>My Erdős number is 3: Mike He [3] → Sanjeev Arora [2] → László Babai [1] → Paul Erdős [0]</li>
</ul></details>
        <details class="personal-details"><summary>Friends &amp; colleagues</summary>
            <p class="small-note">In alphabetical order of last name.</p>
            <ul class="friends-list">{gen_friend_list_html()}</ul>
        </details>
        <details class="personal-details"><summary>Visitors from around the world</summary><img alt="Flag counter" loading="lazy" src="https://s11.flagcounter.com/count2/IatI/bg_FFFFFF/txt_000000/border_CCCCCC/columns_2/maxflags_10/viewers_0/labels_0/pageviews_0/flags_0/percent_0/"/></details>
        <div class="credits"><p>
                    This website is adapted from a template generously provided by <a href="https://m-niemeyer.github.io/" target="_blank">Michael Niemeyer</a>. The Logo of this website is designed by my friend, Melina.
                </p></div>
    </section>
    """
    return name, bio_text, footer

def _build_author_link_map():
    d = {}
    for p in _people_data['people']:
        d[p['name'].lower()] = p['url']
        for alias in p.get('aliases', []):
            d[alias.lower()] = p['url']
    return d

_author_links = _build_author_link_map()

def get_author_link(author):
    author = ''.join(filter(lambda x: x.isalpha() or x in (' ', '-', '.'), author))
    return _author_links.get(author.lower())

def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name={'Mike He', 'Deyuan He'}, add_links=True):
    names = []
    for person in persons:
        name = ' '.join(part for kind in ('first', 'prelast', 'middle', 'last', 'lineage') for part in person.get_part(kind))
        label = escape(name)
        link = get_author_link(name) if add_links else None
        if link:
            label = f'<a href="{escape(link, quote=True)}" target="_blank">{label}</a>'
        if make_bold and name.rstrip('*') in make_bold_name:
            label = f'<strong>{label}</strong>'
        names.append(label)
    return connection.join(names)

def get_paper_entry(entry_key, entry, heading_level=4):
    fields = entry.fields
    title = escape(fields['title'])
    link = fields.get('html') or fields.get('pdf')
    title_html = f'<a href="{escape(link, quote=True)}" target="_blank">{title}</a>' if link else title
    award = f'<span class="award-label">{escape(fields["award"])}</span>' if fields.get('award') else ''
    artefacts = {'html': 'Project', 'pdf': 'Paper', 'supp': 'Supplemental', 'video': 'Video', 'poster': 'Poster', 'code': 'Code'}
    links = ''.join(
        f'<a href="{escape(fields[key], quote=True)}" target="_blank">{label} <span aria-hidden="true">↗</span></a>'
        for key, label in artefacts.items() if fields.get(key)
    )
    badge_names = {
        'artifact_available': ('artifacts_available', 'Artifacts Available'),
        'artifact_functional': ('artifacts_evaluated_functional', 'Artifacts Evaluated — Functional'),
        'artifact_reusable': ('artifacts_evaluated_reusable', 'Artifacts Evaluated — Reusable'),
        'artifact_reproduced': ('results_reproduced', 'Results Reproduced'),
    }
    badges = []
    for key, (filename, label) in badge_names.items():
        if key in fields:
            badge = f'<img src="https://www.acm.org/binaries/content/gallery/acm/publications/artifact-review-v1_1-badges/{filename}_v1_1.png" alt="{label}" loading="lazy">'
            if key == 'artifact_available':
                badge = f'<a href="{escape(fields[key], quote=True)}" target="_blank">{badge}</a>'
            badges.append(badge)
    badge_html = '<div class="artifact-badges">' + ''.join(badges) + '</div>' if badges else ''
    citation = deepcopy(entry)
    for key in list(artefacts) + ['img', 'award'] + list(badge_names):
        citation.fields.pop(key, None)
    cite = escape(citation.to_string('bibtex'))
    venue = escape(fields.get('booktitle', fields.get('journal', 'Preprint')))
    return f"""
    <article class="publication" id="paper-{escape(entry_key, quote=True)}">
        <div class="publication-body">
            <div class="publication-venue">{venue} · {escape(fields['year'])} {award}</div>
            <h{heading_level} class="publication-title">{title_html}</h{heading_level}>
            <p class="publication-authors">{generate_person_html(entry.persons['author'])}</p>
            {badge_html}
            <div class="publication-links">{links}
                <details class="citation"><summary>BibTeX</summary><pre><code>{cite}</code></pre></details>
            </div>
        </div>
    </article>"""

def get_talk_entry(entry, heading_level=3):
    links = ''.join(
        f'<a href="{escape(entry[key], quote=True)}" target="_blank">{label} <span aria-hidden="true">↗</span></a>'
        for key, label in {'slides': 'Slides', 'poster': 'Poster', 'video': 'Recording'}.items() if entry.get(key)
    )
    return f"""
    <article class="talk" id="talk-{escape(entry['id'], quote=True)}">
        <div class="talk-date">{escape(entry['year'])}</div>
        <div class="talk-body"><h{heading_level}>{escape(entry['title'])}</h{heading_level}><p>{escape(entry['venue'])}</p><div class="resource-links">{links}</div></div>
        <img src="{escape(entry['img'], quote=True)}" alt="Figure for {escape(entry['title'], quote=True)}" loading="lazy">
    </article>"""

def _get_intern_stint_html(stint):
    team = f'<p class="career-team">{escape(stint["team"])}</p>' if stint.get('team') else ''
    mentor = escape(stint.get('mentor', ''))
    if stint.get('mentor_page'):
        mentor = f'<a href="{escape(stint["mentor_page"], quote=True)}" target="_blank">{mentor}</a>'
    mentor_html = f'<p class="career-note">Mentor: {mentor}</p>' if mentor else ''
    location = f' · {escape(stint["location"])}' if stint.get('location') else ''
    return f"""<div class="career-stint">
        <p class="career-date">{escape(stint['start_date'])} – {escape(stint['end_date'])}{location}</p>
        {team}<p>{escape(stint['position'])}</p>{mentor_html}
    </div>"""

def get_intern_entry(entry):
    stints = ''.join(_get_intern_stint_html(stint) for stint in entry.get('stints', [entry]))
    return f"""<article class="career-entry">
        <img src="{escape(entry['img'], quote=True)}" alt="" loading="lazy">
        <div><h4><a href="{escape(entry['company_link'], quote=True)}" target="_blank">{escape(entry['company'])}</a></h4>{stints}</div>
    </article>"""

def load_publications():
    """Combine both bibliographies, newest year first; retain order within a year."""
    entries = {}
    for filename in ('publication_list.bib', 'workshops.bib'):
        bib_data = bibtex.Parser().parse_file(filename)
        for key, entry in bib_data.entries.items():
            if key in entries:
                raise ValueError(f'Duplicate publication key: {key}')
            entries[key] = entry
    return sorted(entries.items(), key=lambda item: int(item[1].fields['year']), reverse=True)

def get_selected_publications_html():
    """Category and paper order are configured in selected_publications.json."""
    entries = dict(load_publications())
    with open('selected_publications.json', encoding='utf-8') as f:
        categories = json.load(f)
    sections = []
    selected_keys = set()
    for index, (category, keys) in enumerate(categories.items(), start=1):
        papers = []
        for key in keys:
            if key not in entries:
                raise ValueError(f'Unknown selected publication: {key}')
            if key in selected_keys:
                raise ValueError(f'Duplicate selected publication: {key}')
            selected_keys.add(key)
            papers.append(get_paper_entry(key, entries[key]))
        sections.append(f"""
        <section class="research-category" aria-labelledby="selected-category-{index}">
            <h3 id="selected-category-{index}" class="category-heading"><span aria-hidden="true">0{index}</span>{escape(category)}</h3>
            {''.join(papers)}
        </section>""")
    return ''.join(sections)

def get_publications_page_html():
    papers = ''.join(get_paper_entry(key, entry, heading_level=2) for key, entry in load_publications())
    content = f"""<main id="main" class="page-shell archive-page">
        <header class="archive-header"><p class="eyebrow">Research</p><h1>Publications<span class="accent">.</span></h1>
        <p>Conference and journal publications, preprints, workshop papers, and other contributions.</p>
        <p class="small-note">* denotes a core contributor.</p></header>
        <div class="publication-list">{papers}</div>
        <a class="back-link" href="index.html">← Back to home</a>
    </main>"""
    return get_page_html(content, 'Publications | Mike He', active='publications')

def get_talk_date(talk):
    """Parse the full/abbreviated month dates used in talks.json."""
    for date_format in ('%B %d, %Y', '%b %d, %Y', '%B %Y', '%b %Y'):
        try:
            return datetime.strptime(talk['year'], date_format)
        except ValueError:
            continue
    raise ValueError(f"Unsupported date for talk {talk['id']}: {talk['year']}")

def get_talks_html(limit=None, heading_level=3):
    with open('talks.json', 'r') as f:
        talks = sorted(json.load(f), key=get_talk_date, reverse=True)
    return ''.join(get_talk_entry(t, heading_level=heading_level) for t in talks[:limit])

def get_talks_page_html():
    content = f"""<main id="main" class="page-shell archive-page">
        <header class="archive-header"><p class="eyebrow">Presentations &amp; conversations</p><h1>Talks<span class="accent">.</span></h1>
        <p>Research talks, conference presentations, and posters.</p></header>
        <div class="talk-list">{get_talks_html(heading_level=2)}</div>
        <a class="back-link" href="index.html">← Back to home</a>
    </main>"""
    return get_page_html(content, 'Talks | Mike He', active='talks')

def get_education_entry(entry):
    advisors = []
    for key, label in (('advisor', 'Advisor'), ('co_advisor', 'Co-advisor')):
        if entry.get(key):
            name = escape(entry[key])
            if entry.get(key + '_page'):
                name = f'<a href="{escape(entry[key + "_page"], quote=True)}" target="_blank">{name}</a>'
            advisors.append(f'<p class="career-note">{label}: {name}</p>')
    location = f' · {escape(entry["location"])}' if entry.get('location') else ''
    return f"""<article class="career-entry">
        <img src="{escape(entry['img'], quote=True)}" alt="" loading="lazy">
        <div><h4><a href="{escape(entry['institution_link'], quote=True)}" target="_blank">{escape(entry['institution'])}</a></h4>
        <p class="career-date">{escape(entry['start_date'])} – {escape(entry['end_date'])}{location}</p>
        <p>{entry['degree']}</p>{''.join(advisors)}</div>
    </article>"""

def get_education_html():
    with open('education.json', 'r') as f:
        entries = json.load(f)
    return ''.join(get_education_entry(e) for e in entries)

def get_internship_html():
    with open('internships.json', 'r') as f:
        entries = json.load(f)
    return ''.join(get_intern_entry(e) for e in entries)

def get_professional_activities_html():
    activities = {
        'Reviewer': ["NeurIPS", "IEEE TMC", "AAE@KDD", "SciPy"],
        'Artifact Evaluation': ["POPL", "PLDI", "MLSys", "MICRO"],
        'Sub-reviewer': [],
        'PC': []
    }
    s = """<ul>"""
    for (k, v) in activities.items():
        if v:
            s += f"<li><span style='font-weight: bold;'>{k}</span>: {', '.join(v)}</li>"
    s += """</ul>"""
    return s

def get_page_html(content, title, active='home'):
    """Shared, dependency-free layout for the homepage and research archives."""
    navigation = ''.join(
        f'<a href="{url}"' + (' aria-current="page"' if active == key else '') + f'>{label}</a>'
        for key, label, url in (
            ('home', 'About', 'index.html'),
            ('publications', 'Publications', 'publications.html'),
            ('talks', 'Talks', 'talks.html'),
        )
    )
    s = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Mike He — Ph.D. student at Princeton working on programming languages, formal methods, distributed systems, and safe AI agents.">
    <title>{escape(title)}</title>
    <link rel="icon" type="image/x-icon" href="pictures/AD1024.png">
    <link rel="stylesheet" href="assets/site.css">
</head>
<body>
    <a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header page-shell">
        <a class="wordmark" href="index.html" aria-label="Mike He home">mh<span class="accent">.</span></a>
        <nav aria-label="Main navigation">{navigation}</nav>
    </header>
    {content}
    <footer class="site-footer page-shell"><span>Mike He <span class="footer-dot">/</span> Princeton University</span><a href="#main">Back to top ↑</a></footer>
</body>
</html>
"""
    return '\n'.join(line.rstrip() for line in s.split('\n'))

def get_index_html():
    name, bio_text, footer = get_personal_data()
    content = f"""
    <main id="main" class="page-shell">
        <section class="hero" aria-labelledby="name">
            <div class="hero-intro"><p class="eyebrow">Ph.D. student · Princeton University</p>
                <h1 id="name">{' '.join(name)}<span class="accent">.</span></h1>
                <p class="research-focus">Programming languages. Formal methods.<br>Systems we can reason about.</p>
            </div>
            <figure class="portrait"><img src="assets/img/photo_2025_web.jpg" alt="Mike He" width="483" height="600"><figcaption>Princeton, New Jersey</figcaption></figure>
            <div class="bio">{bio_text}</div>
        </section>
        <section class="site-section research-section" aria-labelledby="publications">
            <div class="section-heading"><h2 id="publications">Selected Publications</h2><a class="text-link" href="publications.html">All publications <span aria-hidden="true">↗</span></a></div>
            <p class="section-note">* denotes a core contributor.</p>
            {get_selected_publications_html()}
        </section>
        <section class="site-section" aria-labelledby="talks">
            <div class="section-heading"><h2 id="talks">Recent Talks</h2><a class="text-link" href="talks.html">All talks <span aria-hidden="true">↗</span></a></div>
            <div class="talk-list">{get_talks_html(limit=3)}</div>
        </section>
        <section class="site-section" aria-labelledby="background">
            <div class="section-heading"><h2 id="background">Background</h2><a class="text-link" href="assets/cv.pdf" target="_blank">Full CV <span aria-hidden="true">↗</span></a></div>
            <div class="background-grid">
                <div><h3 class="eyebrow column-heading">Education</h3>{get_education_html()}
                    <div class="service"><h3 class="eyebrow column-heading">Professional Activities</h3>{get_professional_activities_html()}</div>
                </div>
                <div><h3 class="eyebrow column-heading">Experience</h3>{get_internship_html()}</div>
            </div>
        </section>
        {footer}
    </main>"""
    return get_page_html(content, ' '.join(name))

def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written index content to {filename}.')

def write_publications_html(filename='publications.html'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(get_publications_page_html())
    print(f'Written publications content to {filename}.')

def write_talks_html(filename='talks.html'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(get_talks_page_html())
    print(f'Written talks content to {filename}.')

def load_recordings():
    """Load recordings from recordings.json"""
    with open('recordings.json', 'r') as f:
        return json.load(f)

def get_recordings_by_year():
    """Organize recordings by year"""
    recordings = load_recordings()
    by_year = defaultdict(list)

    for recording in recordings:
        # Extract year from recording_date (format: YYYY-MM)
        year = recording['recording_date'].split('-')[0]
        by_year[year].append(recording)

    # Sort by year (descending)
    return dict(sorted(by_year.items(), key=lambda x: x[0], reverse=True))

def get_all_tags():
    """Get all unique tags from recordings"""
    recordings = load_recordings()
    tags = set()
    for recording in recordings:
        if 'tag' in recording:
            tags.update(recording['tag'])
    return sorted(tags)

def get_recordings_html():
    """A keyboard- and touch-accessible recording archive with native audio controls."""
    recordings_by_year = get_recordings_by_year()
    tag_buttons = ''.join(
        f'<button type="button" class="tag-filter" data-tag="{escape(tag, quote=True)}" aria-pressed="false">{escape(tag)}</button>'
        for tag in get_all_tags()
    )
    years_html = []
    total = 0
    for year, recordings in recordings_by_year.items():
        tracks = []
        for recording in sorted(recordings, key=lambda item: item['recording_date'], reverse=True):
            total += 1
            name = escape(recording['name'])
            source = f'<span class="recording-source">{escape(recording["source"])}</span>' if recording.get('source') else ''
            tags = recording.get('tag', [])
            tag_data = escape(json.dumps(tags), quote=True)
            tag_html = ''.join(f'<span class="recording-tag">{escape(tag)}</span>' for tag in tags)
            audio_path = 'https://only.rs/' + recording['file_path']
            audio_type = 'mpeg' if audio_path.lower().endswith('.mp3') else 'wav'
            date = datetime.strptime(recording['recording_date'], '%Y-%m').strftime('%b %Y')
            size = f'<span>{escape(str(recording["file_size_mb"]))} MB</span>' if recording.get('file_size_mb') else ''
            tracks.append(f"""
            <details class="recording-item" data-tags="{tag_data}">
                <summary><span class="recording-date">{date}</span><span class="recording-label"><span class="recording-name">{name}</span>{source}</span></summary>
                <div class="recording-details">
                    <div class="recording-metadata"><span>{escape(recording.get('composer', 'Unknown composer'))}</span>{size}{tag_html}</div>
                    <audio controls preload="none" class="recording-audio" aria-label="{name}">
                        <source src="{escape(audio_path, quote=True)}" type="audio/{audio_type}">
                        Your browser does not support the audio player.
                    </audio>
                    <p class="audio-error" role="status" hidden>Audio could not be loaded. Try the direct audio link below.</p>
                    <a class="recording-download" href="{escape(audio_path, quote=True)}" target="_blank">Open audio file ↗</a>
                </div>
            </details>""")
        years_html.append(f"""
        <details class="recording-year" open>
            <summary><span class="recording-year-label">{escape(year)}</span> <span class="year-count">{len(recordings)} recording{'s' if len(recordings) != 1 else ''}</span></summary>
            <div class="year-tracks">{''.join(tracks)}</div>
        </details>""")
    content = f"""
    <main id="main" class="page-shell archive-page recordings-page">
        <header class="archive-header">
            <p class="eyebrow">Beyond research</p>
            <h1>Recordings<span class="accent">.</span></h1>
            <p class="recordings-lead">A violin, and a lifelong love of music.</p>
            <p>I have been playing the violin since 2003, long before I started coding. This is a collection of classical pieces and music from games and anime, recorded over the years.</p>
            <details class="recording-story"><summary>A little musical background</summary>
                <p>I was a member of the Philharmonic Orchestra affiliated with the Beijing National Day School from 2012 to 2018 and played as the Principal Second Violin during my high school years. I also played in a quintet ensemble, the Clavichord, with my high school friends for three years.</p>
                <p>My technique isn't what it used to be since college began, when I started studying computer science extensively, but these pieces represent my musical journey.</p>
            </details>
        </header>
        <div class="recordings-toolbar">
            <div class="recording-filters" role="group" aria-label="Filter recordings by category">
                <button type="button" class="tag-filter" data-tag="all" aria-pressed="true">All recordings</button>{tag_buttons}
            </div>
            <div class="recording-list-controls"><p id="recording-count" role="status">{total} recordings</p><button type="button" id="toggle-all-years" aria-expanded="true" aria-controls="recordings-container">Collapse all years</button></div>
        </div>
        <div id="recordings-container">{''.join(years_html)}</div>
        <a class="back-link" href="index.html">← Back to home</a>
    </main>
    <script src="assets/recordings.js" defer></script>
"""
    return get_page_html(content, 'Recordings | Mike He', active='recordings')

def write_recordings_html(filename='recordings.html'):
    """Write recordings page to file"""
    s = get_recordings_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written recordings content to {filename}.')

if __name__ == '__main__':
    write_index_html('index.html')
    write_publications_html('publications.html')
    write_talks_html('talks.html')
    write_recordings_html('recordings.html')
