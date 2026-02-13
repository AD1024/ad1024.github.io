from pybtex.database.input import bibtex
import json
from collections import defaultdict

def friends():
    # last entry is the color for badges colors
    info_list = [
        ('Yinsen (Tesla) Zhang', 'https://ice1000.org/', 'CMU', 'danger'),
        ('Marisa Kirisame', 'https://marisa.moe/', 'Utah', 'danger'),
        ('Yihong Zhang', 'https://effect.systems/', 'UW', 'primary'),
        ('Yinwei Dai', 'https://yinwei-dai.com/', 'Princeton', 'warning'),
        ('Haichen Dong', 'https://haichendong.com/', 'BlackSesame', 'dark'),
        ('Gus Smith', 'https://justg.us/', 'Chipstack', 'primary'),
        ('Vishal Canumalla', 'https://vcanumalla.github.io/', 'Stanford', 'danger'),
        ('Steven Lyubomirsky', 'https://slyubomirsky.github.io/', 'NVIDIA', 'success'),
        ('Altan Haan', 'https://altanh.com/', 'UC Berkeley', 'primary'),
        ('Guanghao Ye', 'https://yeguanghao.xyz/', 'MIT', 'dark'),
        ('Yi Li', 'https://ece.princeton.edu/people/yi-li', 'Meta', 'primary'),
        ('Muru Zhang', 'https://nanami18.github.io/', 'USC', 'danger'),
        ('Shaoqi Wang', 'https://www.linkedin.com/in/shaoqiw/', 'Microsoft', 'primary'),
        ('Thierry Tambe', 'https://thierrytambe.com/', 'Stanford', 'danger'),
        ('Federico Mora Rocha', 'https://federico.morarocha.ca/', 'AWS', 'warning'),
        ('Zhe Zhou', 'https://zhezhouzz.github.io/', 'Purdue', 'dark'),
        ('Yifan Zhu', 'https://www.cs.rochester.edu/~yzhu104/', 'UofR', 'primary'),
        ('Yuyou Fan', 'https://www.linkedin.com/in/yuyou-fan-58085a18b', 'Utah', 'danger'),
        ('Hobart Yang', 'https://discover304.top/', 'MBZUAI', 'light'),
        ('Chenyu Zhou', 'https://self.shiroha.info/', 'USC', 'danger')
    ]
    info_list = sorted(info_list, key=lambda x: x[0].split()[-1])
    return info_list

def gen_friend_list_html():
    friend_list = friends()
    s = []
    for (name, link, school, color) in friend_list:
        content = f"""
<li class="list-group-item d-flex justify-content-between align-items-center">
    <div>
      <div class="fw-bold">{name}</div>
      <a target="_blank" href="{link}" class="text-muted">{link}</a>
    </div>
    <span class="badge rounded-pill badge-{color}">{school}</span>
  </li>"""
        s.append(content)
    return ''.join(s[:len(s) // 2]), ''.join(s[len(s) // 2:])

def get_personal_data():
    name = ["Mike", "He"]
    email = "dh7120@cs.princeton.edu"
    twitter = "1SHL10"
    github = "AD1024"
    linkedin = "deyuan-mike-he"
    bio_text = f"""
                <p>
                    I am a Ph.D. student at the <a target="_blank" href="https://pl.cs.princeton.edu/">Princeton Programming Languages Group</a> advised by Prof. <a target="_blank" href="https://www.cs.princeton.edu/~aartig/"> Aarti Gupta</a>.
                    I am broadly interested in programming languages, formal methods and compilers.
                    My current research focuses on practical formal and semi-formal methods for distributed systems and agentic systems, and I am working with the <a target="_blank" href="https://p-org.github.io/P">P ecosystem</a> for verifying and reasoning about distributed systems.
                </p>
                <p>Before joining Princeton, I studied at the <a target="_blank" href="https://cs.washington.edu">University of Washington</a>, where I was privileged to work with Prof. <a target="_blank" href="https://ztatlock.net/">Zachary Tatlock</a> on equality saturation and its applications to machine learning compilers.
                </p>
                <p>In my free time, I enjoy playing the violin (I've been playing it longer than coding). You can find my archived recordings <a href="recordings.html">here</a>.</p>
                <p>
                    <a class="btn btn-link" type="button" href="./assets/cv.pdf" target="_blank" style="margin-right: 5px"><i class="fa fa-address-card fa-lg"></i> CV</a>
                    <a class="btn btn-link" type="button" href="mailto:{email}" style="margin-right: 5px"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a class="btn btn-link" type="button" href="https://twitter.com/{twitter}" target="_blank" style="margin-right: 5px"><i class="fab fa-twitter fa-lg"></i> Twitter</a>
                    <a class="btn btn-link" type="button" href="https://scholar.google.com/citations?user=dhtWqm8AAAAJ" target="_blank" style="margin-right: 5px"><i class="fa-solid fa-book"></i> Scholar</a>
                    <a class="btn btn-link" type="button" href="https://github.com/{github}" target="_blank" style="margin-right: 5px"><i class="fab fa-github fa-lg"></i> Github</a>
                    <a class="btn btn-link" type="button" href="https://www.linkedin.com/in/{linkedin}" target="_blank" style="margin-right: 5px"><i class="fab fa-linkedin fa-lg"></i> LinkedIn</a>
                    <button data-mdb-ripple-init data-mdb-ripple-color="grey" class="btn btn-link" type="button" data-toggle="collapse" data-target="#demo" data-toggle="collapse"><i class="fa-solid fa-trophy"></i>Awards</button>
                    <div id="demo" class="collapse">
                    <!-- <span style="font-weight: bold;">Awards:</span> -->
                    <ul>
                        <li>2022: <a target="_blank" href="https://news.cs.washington.edu/2022/02/22/allen-school-undergraduates-recognized-by-the-computing-research-association-for-advancing-health-sensing-programming-languages-and-systems-research/">CRA Outstanding Undergraduate Researcher Award, Honorable Mention</a></li>
                        <li>2020: Lynn Conway Research Award (DTR Team)</li>
                        <li>2019: JASSO Scholarship, Waseda University</li>
                        <li>2018 &rarr; 2022: Annual Dean's List, University of Washington</li>
                        <li>2016: NOIp 2nd Prize, Beijing Regional</li>
                    </ul>
                </div>
                </p>
    """
    friend_first_half, friend_second_half = gen_friend_list_html()
    footer = f"""
            <div class="col-sm-12" style="">
                <h4>Misc</h4>
                <ul>
                    <li>I love classical music and enjoy playing the violin. I've been playing the violin for about 20 years.
                     I received the Lv.9 certification issued by the Central Conservatory of Music when I was in middle school.
                    You can find some of my recordings <a href="recordings.html">here</a>.
                    Some video recordings are available @ <a target="_blank" href="https://space.bilibili.com/11936677">Bilibili</a> (the website is in Chinese).</li>
                    <li>I was a part-time translator / proofreading editor in <a target="_blank" href="https://www.youtube.com/channel/UCoSrY_IQQVpmIRZ9Xf-y93g">Gawr Gura</a>'s Chinese fansub team. Gura, now graduated, was a virtual streamer at YouTube affiliated with <a target="_blank" href="https://en.hololive.tv/member">Hololive Production</a> (EN).</li>
                    <li>My Erdős number is 3: Mike He [3] &rarr; Sanjeev Arora [2] &rarr; László Babai [1] &rarr; Paul Erdős [0]</li>
                </ul>
                <h4>Friends and Colleagues (by alphabetical order of last names)</h4>
                <div class="row justify-content-center pe-3 ps-3">
                    <ul class="col-sm-5 list-group list-group-light">
                        {friend_first_half}
                    </ul>
                    <ul class="col-sm-5 list-group list-group-light">
                        {friend_second_half}
                    </ul>
                </div>
                <hr/>
                <h4>Visitors are welcomed!</h4>
                <img src="https://s11.flagcounter.com/count2/IatI/bg_FFFFFF/txt_000000/border_CCCCCC/columns_2/maxflags_10/viewers_0/labels_0/pageviews_0/flags_0/percent_0/"/>
                <p>
                    This website is adapted from a template generously provided by <a target="_blank" href="https://m-niemeyer.github.io/">Michael Niemeyer</a>.
                </p>
            </div>
    """
    return name, bio_text, footer

def get_author_link(author):
    author = ''.join(filter(lambda x: x.isalpha() or x in (' ', '-', '.'), author))
    author = author.lower()
    d = {
        # 'Deyuan He': 'https://www.cs.princeton.edu/~dh7120/',
        'Zachary Tatlock': 'https://ztatlock.net/',
        'Aarti Gupta': 'https://www.cs.princeton.edu/~aartig/',
        'Sharad Malik': 'https://www.princeton.edu/~sharad/',  
        'Haichen Dong': 'https://haichendong.com/',
        'Gus Henry Smith': 'https://justg.us/',
        'Gus Smith': 'https://justg.us/',
        'Vishal Canumalla': 'https://vcanumalla.github.io/',
        'Steven Lyubomirsky': 'https://slyubomirsky.github.io/',
        'Marisa Kirisame': 'https://marisa.moe/',
        'Jennifer Brennan': 'https://jenniferbrennan.github.io/',
        'Yi Li': 'https://ece.princeton.edu/people/yi-li',
        'Gu-Yeon Wei': 'https://seas.harvard.edu/person/gu-yeon-wei',
        'Thierry Tambe': 'https://thierrytambe.com/',
        'Jared Roesch': 'https://jroesch.github.io/',
        'Tianqi Chen': 'https://tqchen.com/',
        'Bo-yuan Huang': 'https://boyuanhuang.com/',
        'Akash Gaonkar': 'https://scholar.google.com/citations?user=Ccvj2usAAAAJ&hl=en',
        'Altan Haan': 'https://altanh.com/',
        'Ankush Desai': 'https://ankushdesai.github.io/',
        'Aishwarya Jagarapu': 'https://www.linkedin.com/in/aishwarya-jagarapu/',
        'Doug Terry': 'https://www.amazon.science/author/douglas-terry',
        'Andrew Cheung': 'https://ninehusky.github.io/',
        'Scale AI': 'https://scale.com/',
        'Center for AI Safety': 'https://safe.ai/',
        'Zhendong Ang': 'https://ang9876.github.io/',
        'Haoyu Zhao': 'https://hyzhao.me/',
        'Ziran Yang': 'https://ziranyang0.github.io/',
        'Jiawei Li': 'https://ece.illinois.edu/about/directory/grad-students/jiaweil9',
        'Zenan Li': 'https://lizn-zn.github.io/',
        'Chi Jin': 'https://sites.google.com/view/cjin/home',
        'Venugopal V. Veeravalli': 'https://vvv.ece.illinois.edu/',
        'Sanjeev Arora': 'https://www.cs.princeton.edu/~arora/'
    }
    d = {
        k.lower(): v for k, v in d.items()
    }
    return d.get(author)

def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name={'Mike He', 'Deyuan He'}, add_links=True):
    s = ""
    for p in persons:
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('prelast') + p.get_part('middle') + p.get_part('last') + p.get_part('lineage'): 
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if add_links:
            link = get_author_link(string_part_i)
            if link and add_links:
                string_part_i = f'<a href="{link}" target="_blank">{string_part_i}</a>'
        if make_bold and ''.join(filter(lambda x: x.isalpha() or x in (' ', '-', '.'), string_part_i)) in make_bold_name:
            string_part_i = f'<span style="font-weight: bold";>{string_part_i}</span>'
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_paper_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<div class="thumb-zoom-container" style="--zoom-img: url('{entry.fields['img']}')"><img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image"></div>"""
    s += """</div><div class="col-sm-9">"""

    link = entry.fields.get('html', entry.fields.get('pdf', ''))
    if 'award' in entry.fields.keys():
        s += f"""<a style="font-size: 13pt" href="{link}" target="_blank"><strong>{entry.fields['title']}</strong></a> <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        s += f"""<a style="font-size: 13pt" href="{link}" target="_blank"><strong>{entry.fields['title']}</strong></a> <br>"""
    s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    s += f"""<span style="font-style: italic;">{entry.fields.get('booktitle', entry.fields.get('journal', 'Pre-print'))}</span>, {entry.fields['year']} <br>"""

    artefacts = {'html': 'Project Page', 'pdf': 'Paper', 'supp': 'Supplemental', 'video': 'Video', 'poster': 'Poster', 'code': 'Code'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            # if i > 0:
            #     s += ' / '
            s += f"""<a class="btn btn-link" type="button" href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')

    # cite = "<pre><code>@article{" + f"{entry_key}, \n"
    # cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    # for entr in ['title', 'booktitle', 'year']:
    #     cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    # cite += """}</pre></code>"""
    for key in list(artefacts.keys()) + ['img', 'award']:
        if key in entry.fields.keys():
            del entry.fields[key]
    cite = "<pre><code>{}</code></pre>".format(entry.to_string("bibtex"))
    s += f"""<button data-mdb-ripple-init data-mdb-ripple-color="pink" class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Expand bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    s += """ </div> </div> </div>"""
    return s

def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""<strong>{entry.fields['title']}</strong><br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'slides': 'Slides', 'video': 'Recording'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    s += """ </div> </div> </div>"""
    return s

def get_intern_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<div
  class="bg-image hover-overlay shadow-1-strong rounded"
  style="height: 128px; width: 128px;"
  data-mdb-ripple-init
  data-mdb-ripple-color="light"
><img src="{entry.fields['img']}" width=128 height=128 class="img-fluid img-thumbnail" alt="company logo">
<a target="_blank" href="{entry.fields['company_link']}">
    <div class="mask" style="background: linear-gradient(
        45deg,
        hsla(168, 85%, 52%, 0.5),
        hsla(263, 88%, 45%, 0.5) 100%
      );"></div>
</a>
</div>"""
    s += """</div><div class="col-sm-9">"""
    s += f"""<strong>{entry.fields['company']}</strong>, {entry.fields['start_date']} &rarr; {entry.fields['end_date']}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['position']}</span><br>"""
    if 'mentor' in entry.fields.keys():
        if 'mentor_page' in entry.fields.keys():
            s += f"""<a href="{entry.fields['mentor_page']}" target="_blank"><span class="badge badge-pill badge-primary">Mentor: {entry.fields['mentor']}</span></a>"""
        else:
            s += f"""<span class="badge badge-pill badge-primary">Mentor: {entry.fields['mentor']}</span>"""
        s += "<br>"
    if 'location' in entry.fields.keys():
        s += f"""<span class="badge badge-pill badge-secondary">{entry.fields['location']}</span>"""
    s += """ </div> </div> </div>"""
    return s

def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_paper_entry(k, bib_data.entries[k])
    return s

def get_workshop_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('workshops.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_paper_entry(k, bib_data.entries[k])
    return s

def get_talks_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('talk_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_talk_entry(k, bib_data.entries[k])
    return s

def get_education_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<a target="_blank" href="{entry.fields['institution_link']}"><img src="{entry.fields['img']}" width=98 height=98 class="img-fluid" alt="institution logo"></a>"""
    s += """</div><div class="col-sm-9">"""
    if 'location' in entry.fields.keys():
        location = entry.fields['location']
    else:
        location = ""
    s += f"""<strong>{entry.fields['institution']}</strong>{(", " + location) if location else ", "} {entry.fields['start_date']} &rarr; {entry.fields['end_date']}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['degree']}</span><br>"""
    if 'advisor' in entry.fields.keys():
        if 'advisor_page' in entry.fields.keys():
            s += f"""<a href="{entry.fields['advisor_page']}" target="_blank"><span class="badge badge-pill badge-primary">Advisor: {entry.fields['advisor']}</span></a>"""
        else:
            s += f"""<span class="badge badge-pill badge-primary">Advisor: {entry.fields['advisor']}</span>"""
    if 'co_advisor' in entry.fields.keys():
        if 'co_advisor_page' in entry.fields.keys():
            s += f"""    <a href="{entry.fields['co_advisor_page']}" target="_blank"><span class="badge badge-pill badge-primary">Co-Advisor: {entry.fields['co_advisor']}</span></a>"""
        else:
            s += f"""<span class="badge badge-pill badge-primary">Co-Advisor: {entry.fields['co_advisor']}</span>"""
        s += "<br>"
    s += """ </div> </div> </div>"""
    return s

def get_education_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('education.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_education_entry(k, bib_data.entries[k])
    return s

def get_internship_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('internships.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_intern_entry(k, bib_data.entries[k])
    return s

def get_professional_activities_html():
    activities = {
        'Reviewer': ["IEEE TMC", "AAE'25@KDD", "SciPy'25"],
        'Artifact Evaluation Committee': ["POPL'25", "PLDI'24", "POPL'24", "MLSys'23", "MICRO'21"],
        'Sub-reviewer': ["OOPSLA'24"],
        'PC': []
    }
    s = """<ul>"""
    for (k, v) in activities.items():
        if v:
            s += f"<li><span style='font-weight: bold;'>{k}</span>: {', '.join(v)}</li>"
    s += """</ul>"""
    return s

def get_index_html():
    pub = get_publications_html()
    talks = get_talks_html()
    name, bio_text, footer = get_personal_data()
    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <!-- Google Fonts -->
<link
  href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
  rel="stylesheet"
/>
<!-- MDB -->
<link
  href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.2.0/mdb.min.css"
  rel="stylesheet"
/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <title>{name[0] + ' ' + name[1]}</title>
  <link rel="icon" type="image/x-icon" href="pictures/AD1024.png">
  <style>
  a {{
  text-decoration: underline solid transparent;
  transition: text-decoration 0.3s ease;
}}

a:hover {{
  text-decoration: underline solid Currentcolor;
}}
.thumb-zoom-container {{
  position: relative;
}}
.thumb-zoom-container img {{
  transition: opacity 0.2s ease;
}}
.thumb-zoom-container:hover img {{
  opacity: 0.85;
}}
.thumb-zoom-container::after {{
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background-image: inherit;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 4px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  opacity: 0;
  pointer-events: none;
  transition: all 0.2s ease;
  z-index: 100;
}}
.thumb-zoom-container:hover::after {{
  content: '';
  position: absolute;
  top: 50%;
  left: 100%;
  transform: translateY(-50%);
  margin-left: 10px;
  width: 400px;
  height: 300px;
  background-image: var(--zoom-img);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  opacity: 1;
  pointer-events: none;
  z-index: 100;
}}
  </style>
</head>

<body>
    <div class="container">
        <div class="row ps-2 pe-2">
            <div class="col-md-1"></div>
            <div class="col-md-10">
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="margin-bottom: 1em;">
                    <h3 class="display-4" style="text-align: center;"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3>
                    </div>
                    <br>
                    <div class="col-md-10" style="">
                        {bio_text}
                    </div>
                    <div class="col-md-2" style="">
                        <img src="assets/img/photo_2025.jpg" class="img-thumbnail" width="280px" alt="Profile picture">
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Conference / Journal Publications &amp; Pre-prints</h4>
                        <div><p>(*: Equal contribution)</p></div>
                        {pub}
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Misc. Projects &amp Short Papers</h4>
                        <div><p>(*: Equal contribution)</p></div>
                        {get_workshop_html()}
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Education</h4>
                        {get_education_html()}
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Experience</h4>
                        {get_internship_html()}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="">
                        <h4>Talks</h4>
                        {talks}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="">
                        <h4>Professional Activities</h4>
                        {get_professional_activities_html()}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em; margin-bottom: 1em;">
                    {footer}
                </div>
            </div>
            <div class="col-md-1"></div>
        </div?
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.2.0/mdb.umd.min.js"></script>
</body>

</html>
    """
    return s


def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written index content to {filename}.')

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
    """Generate HTML for recordings portfolio page"""
    recordings_by_year = get_recordings_by_year()
    all_tags = get_all_tags()

    # Generate tag badges with filter functionality
    tag_badges = []
    tag_colors = {
        'Classical': 'primary',
        'Game OST': 'success',
        'Anime OST': 'danger'
    }

    for tag in all_tags:
        color = tag_colors.get(tag, 'secondary')
        tag_badges.append(
            f'<span class="badge badge-{color} tag-filter" style="cursor: pointer; margin: 2px;" data-tag="{tag}">{tag}</span>'
        )

    tags_html = ' '.join(tag_badges)

    # Generate recordings by year
    recordings_html = []
    for year, recordings in recordings_by_year.items():
        recordings_html.append(f'<h5 class="mt-4 year-title" data-year="{year}">{year}</h5>')

        for recording in recordings:
            # Build display name
            display_name = recording['name']
            if 'source' in recording:
                display_name += f' <span style="font-style: italic;">(from {recording["source"]})</span>'

            # Build tags
            tags = recording.get('tag', [])
            tag_html = []
            for tag in tags:
                color = tag_colors.get(tag, 'secondary')
                tag_html.append(f'<span class="badge badge-{color} recording-tag">{tag}</span>')
            tags_display = ' '.join(tag_html)

            # Recording date
            recording_date = recording['recording_date']

            # Composer
            composer = recording.get('composer', 'Unknown')

            # File size
            file_size = recording.get('file_size_mb', 'N/A')

            # Audio file path
            audio_path = 'https://only.rs/' + recording['file_path']

            # Create recording card with data attributes for filtering
            tag_data = ','.join(tags)
            recording_card = f'''
<div class="recording-item card mb-2" data-tags="{tag_data}" data-year="{year}">
    <div class="card-body">
        <h6 class="card-title mb-0">
            {display_name}
            <span class="expand-icon">▼</span>
        </h6>
        <div class="recording-details">
            <hr class="my-2">
            <p class="card-text mb-1">
                <strong>Composer:</strong> {composer}<br>
                <strong>Recorded:</strong> {recording_date}<br>
                <strong>Size:</strong> {file_size} MB<br>
                {tags_display}
            </p>
            <audio preload="none" class="w-100 mt-2 recording-audio">
                <source src="{audio_path}" type="audio/{'mpeg' if audio_path.endswith('.mp3') else 'wav'}">
                Your browser does not support the audio element.
            </audio>
            <div class="music-player mt-2">
                <button class="play-btn btn btn-primary btn-sm" data-mdb-ripple-init data-mdb-ripple-color="light">
                    <i class="fas fa-play"></i>
                </button>
                <div class="timeline-container">
                    <div class="timeline">
                        <div class="playhead"></div>
                    </div>
                </div>
                <span class="time-display">
                    <span class="current-time">0:00</span> / <span class="duration">0:00</span>
                </span>
            </div>
        </div>
    </div>
</div>'''
            recordings_html.append(recording_card)

    recordings_content = '\n'.join(recordings_html)

    # Generate full page HTML
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" rel="stylesheet"/>
  <!-- MDB -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.2.0/mdb.min.css" rel="stylesheet"/>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <title>Mike He - Recordings</title>
  <link rel="icon" type="image/x-icon" href="pictures/AD1024.png">

  <style>
    a {{
      text-decoration: underline solid transparent;
      transition: text-decoration 0.3s ease;
    }}
    a:hover {{
      text-decoration: underline solid Currentcolor;
    }}
    .tag-filter {{
      user-select: none;
    }}
    .tag-filter:hover {{
      opacity: 0.8;
    }}
    .tag-filter.active {{
      box-shadow: 0 0 0 2px #000;
      font-weight: bold;
    }}
    .recording-item {{
      cursor: pointer;
      transition: all 0.3s ease;
    }}
    .recording-item.hidden {{
      display: none;
    }}
    .recording-item.year-collapsed {{
      display: none;
    }}
    .recording-item:hover {{
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
      transform: translateY(-2px);
    }}
    .year-title {{
      transition: opacity 0.3s ease;
      cursor: pointer;
      user-select: none;
    }}
    .year-title:hover {{
      color: #007bff;
    }}
    .year-title.hidden {{
      display: none;
    }}
    .year-title::after {{
      content: ' ▼';
      font-size: 0.8em;
      color: #666;
      transition: transform 0.3s ease;
      display: inline-block;
    }}
    .year-title.collapsed::after {{
      transform: rotate(-90deg);
    }}
    .recording-details {{
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.3s ease;
    }}
    .recording-item.expanded .recording-details {{
      max-height: 300px;
    }}
    .expand-icon {{
      transition: transform 0.3s ease;
      float: right;
      color: #666;
    }}
    .recording-item.expanded .expand-icon {{
      transform: rotate(180deg);
    }}
    .music-player {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px;
      background: #f8f9fa;
      border-radius: 8px;
    }}
    .play-btn {{
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0;
      flex-shrink: 0;
      transition: all 0.3s ease;
      box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    .play-btn:hover {{
      transform: scale(1.1);
      box-shadow: 0 4px 12px rgba(0,123,255,0.4);
    }}
    .play-btn:active {{
      transform: scale(0.95);
    }}
    .timeline-container {{
      flex: 1;
      padding: 0 10px;
    }}
    .timeline {{
      width: 100%;
      height: 6px;
      background: #ddd;
      border-radius: 3px;
      position: relative;
      cursor: pointer;
    }}
    .playhead {{
      position: absolute;
      left: 0;
      top: 0;
      height: 100%;
      background: #007bff;
      border-radius: 3px;
      width: 0%;
      transition: width 0.1s linear;
    }}
    .time-display {{
      font-size: 0.85em;
      color: #666;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .recording-audio {{
      display: none;
    }}
  </style>
</head>

<body>
  <div class="container">
    <div class="row ps-2 pe-2">
      <div class="col-md-1"></div>
      <div class="col-md-10">
        <div class="row" style="margin-top: 3em; margin-bottom: 2em;">
          <div class="col-sm-12">
            <h3 class="display-4" style="text-align: center;">
              <a href="index.html" style="text-decoration: none; color: inherit;">
                <span style="font-weight: bold;">Mike</span> He
              </a>
            </h3>
            <p style="text-align: center;">
              <a href="index.html">← Back to main page</a>
            </p>
          </div>
        </div>

        <div class="row">
          <div class="col-sm-12">
            <h4>Violin Recording Archive</h4>
            <p>I have been playing the violin since 2003, way before I started coding. I was a member of the Philharmonic Orchestra affiliated with the Beijing National Day School from 2012 to 2018 and played as the Principal Second Violin during my high school years. I also played in a quintet ensemble (named the Clavichord) with my high school friends for 3 years.</p>
            <p>Here's a collection of my violin recordings from over the years. My technique isn't what it used to be since college began (when I started studying computer science extensively), but these pieces represent my musical journey. Filter by category using the tags below—collapsing any section will pause the audio. Moreover, it guarantees "Mutual exclusion": <strong>at most one audio can be played at a time.</strong></p>

            <div class="mb-3">
              <strong>Filter by tags:</strong><br>
              <span class="badge badge-secondary tag-filter active" style="cursor: pointer; margin: 2px;" data-tag="all">All</span>
              {tags_html}
            </div>

            <div class="mb-3">
              <button id="toggle-all-years" class="btn btn-sm btn-outline-primary">
                <i class="fas fa-compress-alt"></i> Collapse All Years
              </button>
            </div>

            <div id="recordings-container">
              {recordings_content}
            </div>
          </div>
        </div>

        <div class="row" style="margin-top: 2em; margin-bottom: 2em;">
          <div class="col-sm-12">
            <hr/>
            <p style="text-align: center;">
              <a href="index.html">← Back to main page</a>
            </p>
          </div>
        </div>
      </div>
      <div class="col-md-1"></div>
    </div>
  </div>

  <!-- JavaScript -->
  <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
    integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
    crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
    integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
    crossorigin="anonymous"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
    integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
    crossorigin="anonymous"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.2.0/mdb.umd.min.js"></script>

  <script>
    // Tag filtering functionality
    document.addEventListener('DOMContentLoaded', function() {{
      const tagFilters = document.querySelectorAll('.tag-filter');
      const recordings = document.querySelectorAll('.recording-item');
      const yearTitles = document.querySelectorAll('.year-title');
      const toggleAllBtn = document.getElementById('toggle-all-years');
      let allCollapsed = false;

      // Helper function to stop audio in a recording card
      function stopAudio(recording) {{
        const audio = recording.querySelector('audio');
        if (audio) {{
          audio.pause();
        }}
        const playBtn = recording.querySelector('.play-btn');
        if (playBtn) {{
          playBtn.innerHTML = '<i class="fas fa-play"></i>';
        }}
      }}

      // Initialize custom music players
      recordings.forEach(recording => {{
        const audio = recording.querySelector('.recording-audio');
        const playBtn = recording.querySelector('.play-btn');
        const timeline = recording.querySelector('.timeline');
        const playhead = recording.querySelector('.playhead');
        const currentTimeSpan = recording.querySelector('.current-time');
        const durationSpan = recording.querySelector('.duration');

        if (!audio || !playBtn) return;

        // Format time helper
        function formatTime(seconds) {{
          const mins = Math.floor(seconds / 60);
          const secs = Math.floor(seconds % 60);
          return `${{mins}}:${{secs.toString().padStart(2, '0')}}`;
        }}

        // Load metadata
        audio.addEventListener('loadedmetadata', function() {{
          durationSpan.textContent = formatTime(audio.duration);
        }});

        // Update time display
        audio.addEventListener('timeupdate', function() {{
          const percentage = (audio.currentTime / audio.duration) * 100;
          playhead.style.width = percentage + '%';
          currentTimeSpan.textContent = formatTime(audio.currentTime);
        }});

        // Play/pause button
        playBtn.addEventListener('click', function(e) {{
          e.stopPropagation();

          // Pause all other audios
          document.querySelectorAll('.recording-audio').forEach(otherAudio => {{
            if (otherAudio !== audio && !otherAudio.paused) {{
              otherAudio.pause();
              const otherRecording = otherAudio.closest('.recording-item');
              if (otherRecording) {{
                stopAudio(otherRecording);
              }}
            }}
          }});

          if (audio.paused) {{
            audio.play();
            playBtn.innerHTML = '<i class="fas fa-pause"></i>';
          }} else {{
            audio.pause();
            playBtn.innerHTML = '<i class="fas fa-play"></i>';
          }}
        }});

        // Seek functionality
        timeline.addEventListener('click', function(e) {{
          e.stopPropagation();
          const rect = timeline.getBoundingClientRect();
          const clickX = e.clientX - rect.left;
          const percentage = clickX / rect.width;
          audio.currentTime = percentage * audio.duration;
        }});

        // Reset on end
        audio.addEventListener('ended', function() {{
          playBtn.innerHTML = '<i class="fas fa-play"></i>';
          playhead.style.width = '0%';
          audio.currentTime = 0;
        }});
      }});

      // Toggle all years button
      toggleAllBtn.addEventListener('click', function() {{
        allCollapsed = !allCollapsed;

        yearTitles.forEach(yearTitle => {{
          const year = yearTitle.getAttribute('data-year');
          const yearRecordings = Array.from(recordings).filter(
            r => r.getAttribute('data-year') === year
          );

          if (allCollapsed) {{
            // Collapse all years
            yearTitle.classList.add('collapsed');
            yearRecordings.forEach(recording => {{
              recording.classList.add('year-collapsed');
              if (recording.classList.contains('expanded')) {{
                recording.classList.remove('expanded');
                stopAudio(recording);
              }}
            }});
          }} else {{
            // Expand all years
            yearTitle.classList.remove('collapsed');
            yearRecordings.forEach(recording => {{
              recording.classList.remove('year-collapsed');
            }});
          }}
        }});

        // Update button text and icon
        if (allCollapsed) {{
          toggleAllBtn.innerHTML = '<i class="fas fa-expand-alt"></i> Expand All Years';
        }} else {{
          toggleAllBtn.innerHTML = '<i class="fas fa-compress-alt"></i> Collapse All Years';
        }}
      }});

      // Year collapse/expand functionality
      yearTitles.forEach(yearTitle => {{
        yearTitle.addEventListener('click', function() {{
          const year = this.getAttribute('data-year');
          const isCollapsed = this.classList.contains('collapsed');

          // Toggle collapsed state
          this.classList.toggle('collapsed');

          // Find all recordings for this year
          const yearRecordings = Array.from(recordings).filter(
            r => r.getAttribute('data-year') === year
          );

          // Toggle visibility and stop audio if collapsing
          yearRecordings.forEach(recording => {{
            if (isCollapsed) {{
              recording.classList.remove('year-collapsed');
            }} else {{
              recording.classList.add('year-collapsed');
              // Stop audio and collapse card when hiding year
              if (recording.classList.contains('expanded')) {{
                recording.classList.remove('expanded');
                stopAudio(recording);
              }}
            }}
          }});

          // Update the toggle-all button state based on current year states
          const allYearsCollapsed = Array.from(yearTitles).every(yt => yt.classList.contains('collapsed'));
          const noYearsCollapsed = Array.from(yearTitles).every(yt => !yt.classList.contains('collapsed'));

          if (allYearsCollapsed) {{
            allCollapsed = true;
            toggleAllBtn.innerHTML = '<i class="fas fa-expand-alt"></i> Expand All Years';
          }} else if (noYearsCollapsed) {{
            allCollapsed = false;
            toggleAllBtn.innerHTML = '<i class="fas fa-compress-alt"></i> Collapse All Years';
          }}
        }});
      }});

      // Expand/collapse recording cards
      recordings.forEach(recording => {{
        recording.addEventListener('click', function(e) {{
          // Don't toggle if clicking on audio controls
          if (e.target.tagName === 'AUDIO' || e.target.closest('audio')) {{
            return;
          }}

          const wasExpanded = this.classList.contains('expanded');

          // Collapse all other cards and stop their audio
          recordings.forEach(other => {{
            if (other !== this && other.classList.contains('expanded')) {{
              other.classList.remove('expanded');
              stopAudio(other);
            }}
          }});

          // Toggle current card
          if (wasExpanded) {{
            this.classList.remove('expanded');
            stopAudio(this);
          }} else {{
            this.classList.add('expanded');
          }}
        }});
      }});

      tagFilters.forEach(filter => {{
        filter.addEventListener('click', function() {{
          const selectedTag = this.getAttribute('data-tag');

          // Update active state
          tagFilters.forEach(f => f.classList.remove('active'));
          this.classList.add('active');

          // Filter recordings
          recordings.forEach(recording => {{
            const recordingTags = recording.getAttribute('data-tags').split(',');

            if (selectedTag === 'all' || recordingTags.includes(selectedTag)) {{
              recording.classList.remove('hidden');
            }} else {{
              recording.classList.add('hidden');
              // Stop audio and collapse if being hidden
              if (recording.classList.contains('expanded')) {{
                recording.classList.remove('expanded');
                stopAudio(recording);
              }}
            }}
          }});

          // Hide year titles if no recordings are visible for that year
          yearTitles.forEach(yearTitle => {{
            const year = yearTitle.getAttribute('data-year');
            const recordingsInYear = Array.from(recordings).filter(
              r => r.getAttribute('data-year') === year
            );
            const hasVisibleRecordings = recordingsInYear.some(
              r => !r.classList.contains('hidden')
            );

            if (hasVisibleRecordings) {{
              yearTitle.classList.remove('hidden');
            }} else {{
              yearTitle.classList.add('hidden');
            }}
          }});
        }});
      }});
    }});
  </script>
</body>
</html>'''

    return html

def write_recordings_html(filename='recordings.html'):
    """Write recordings page to file"""
    s = get_recordings_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written recordings content to {filename}.')

if __name__ == '__main__':
    write_index_html('index.html')
    write_recordings_html('recordings.html')