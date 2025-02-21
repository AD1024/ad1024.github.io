from pybtex.database.input import bibtex

def friends():
    # last entry is the color for badges colors
    info_list = [
        ('Yinsen (Tesla) Zhang', 'https://ice1000.org/', 'CMU', 'danger'),
        ('Marisa Kirisame', 'https://marisa.moe/', 'Utah', 'danger'),
        ('Yihong Zhang', 'https://effect.systems/', 'UW', 'primary'),
        ('Yinwei Dai', 'https://yinwei-dai.com/', 'Princeton', 'warning'),
        ('Haichen Dong', 'https://haichendong.com/', 'Princeton', 'warning'),
        ('Gus Smith', 'https://justg.us/', 'UW', 'primary'),
        ('Vishal Canumalla', 'https://vcanumalla.github.io/', 'Stanford', 'danger'),
        ('Steven Lyubomirsky', 'https://slyubomirsky.github.io/', 'OctoML', 'primary'),
        ('Altan Haan', 'https://altanh.com/', 'UC Berkeley', 'primary'),
        ('Guanghao Ye', 'https://yeguanghao.xyz/', 'MIT', 'dark'),
        ('Yi Li', 'https://ece.princeton.edu/people/yi-li', 'Meta', 'primary'),
        ('Muru Zhang', 'https://nanami18.github.io/', 'UW', 'primary'),
        ('Shaoqi Wang', 'https://www.linkedin.com/in/shaoqiw/', 'NEU', 'danger'),
        ('Thierry Tambe', 'https://thierrytambe.com/', 'Stanford', 'danger'),
        ('Federico Mora Rocha', 'https://federico.morarocha.ca/', 'UC Berkeley', 'primary'),
        ('Zhe Zhou', 'https://zhezhouzz.github.io/', 'Purdue', 'dark'),
        ('Yifan Zhu', 'https://www.cs.rochester.edu/~yzhu104/Main.html', 'Rochester', 'primary'),
        ('Yuyou Fan', 'https://www.linkedin.com/in/yuyou-fan-58085a18b', 'Utah', 'danger'),
        ('Hobart Yang', 'https://discover304.top/', 'MBZUAI', 'light'), # reverted for pending affiliation
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
                    I am a 3rd-year Ph.D. at the <a target="_blank" href="https://www.cs.princeton.edu/"> Department of Computer Science</a>, Princeton University advised by Prof. <a target="_blank" href="https://www.cs.princeton.edu/~aartig/"> Aarti Gupta</a>. I also obtained a M.A. in Computer Science from Princeton University. Before joining Princeton, I received my B.S. in Computer Science from the <a target="_blank" href="https://cs.washington.edu">University of Washington</a>. I was fortunate to work with Prof. <a target="_blank" href="https://ztatlock.net/">Zachary Tatlock</a> on formal methods, machine learning systems and equality saturation. My research focuses on building accessible tools for enabling practical formal methods on real-world systems. Specifically, I am working on verification infrastructures for distributed systems. 
                </p>
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
                    Here is a <a target="_blank" href="assets/Meditation.mp3">sample recording</a> (Meditation from Thais) made in Dec. 2023.
                    Some other recordings are available @ <a target="_blank" href="https://space.bilibili.com/11936677">Bilibili</a> (the website is in Chinese).</li>
                    <li>I was a part-time translator / proofreading editor in <a target="_blank" href="https://www.youtube.com/channel/UCoSrY_IQQVpmIRZ9Xf-y93g">Gawr Gura</a>'s Chinese fansub team. Gura is a virtual streamer at YouTube affiliated with <a target="_blank" href="https://en.hololive.tv/member">Hololive Production</a> (EN).</li>
                    <li>My Erdős number is 4</li>
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
        'Deyuan He': 'https://www.cs.princeton.edu/~dh7120/',
        'Zachary Tatlock': 'https://ztatlock.net/',
        'Aarti Gupta': 'https://www.cs.princeton.edu/~aartig/',
        'Sharad Malik': 'https://www.princeton.edu/~sharad/',  
        'Haichen Dong': 'https://haichendong.com/',
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
    }
    d = {
        k.lower(): v for k, v in d.items()
    }
    return d.get(author)

def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name='Mike He', add_links=True):
    s = ""
    for p in persons:
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'): 
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if add_links:
            link = get_author_link(string_part_i)
            if link and add_links:
                string_part_i = f'<a href="{link}" target="_blank">{string_part_i}</a>'
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold";>{make_bold_name}</span>'
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_paper_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""

    if 'award' in entry.fields.keys():
        s += f"""<a style="font-size: 13pt" href="{entry.fields['html']}" target="_blank"><strong>{entry.fields['title']}</strong></a> <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        s += f"""<a style="font-size: 13pt" href="{entry.fields['html']}" target="_blank"><strong>{entry.fields['title']}</strong></a> <br>"""

    s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

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

    cite = "<pre><code>@InProceedings{" + f"{entry_key}, \n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    for entr in ['title', 'booktitle', 'year']:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
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
                        <img src="assets/img/photo.png" class="img-thumbnail" width="280px" alt="Profile picture">
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Publications &amp; Workshops</h4>
                        <div><p>(*: Equal contribution)</p></div>
                        {pub}
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

if __name__ == '__main__':
    write_index_html('index.html')