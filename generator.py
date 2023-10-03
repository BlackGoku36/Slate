import json
import os
from subprocess import Popen, PIPE
import shutil
import sys
import shutil

# UTIL functions ------

def create_dir(file_path):
    try:
        os.mkdir(file_path)
    except:
        x = 0

def remove_dir(file_path):
    try:
        shutil.rmtree(file_path)
    except:
        x = 0

# UTIL functions ------

path_to_pandoc = 'pandoc'
try:
    path_to_pandoc = sys.argv[1]
except:
    print('Trying installed pandoc at PATH')

profile = {}
blogs = []
contacts = []

mailSVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-mail">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
            </svg>'''
twitterSVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-twitter">
                <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z">
                </path>
            </svg>'''
githubSVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-github">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22">
                </path>
            </svg>'''

mastodonSVG = '''
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21.327 8.566c0-4.339-2.843-5.61-2.843-5.61-1.433-.658-3.894-.935-6.451-.956h-.063c-2.557.021-5.016.298-6.45.956 0 0-2.843 1.272-2.843 5.61 0 .993-.019 2.181.012 3.441.103 4.243.778 8.425 4.701 9.463 1.809.479 3.362.579 4.612.51 2.268-.126 3.541-.809 3.541-.809l-.075-1.646s-1.621.511-3.441.449c-1.804-.062-3.707-.194-3.999-2.409a4.523 4.523 0 0 1-.04-.621s1.77.433 4.014.536c1.372.063 2.658-.08 3.965-.236 2.506-.299 4.688-1.843 4.962-3.254.434-2.223.398-5.424.398-5.424zm-3.353 5.59h-2.081V9.057c0-1.075-.452-1.62-1.357-1.62-1 0-1.501.647-1.501 1.927v2.791h-2.069V9.364c0-1.28-.501-1.927-1.502-1.927-.905 0-1.357.546-1.357 1.62v5.099H6.026V8.903c0-1.074.273-1.927.823-2.558.566-.631 1.307-.955 2.228-.955 1.065 0 1.872.409 2.405 1.228l.518.869.519-.869c.533-.819 1.34-1.228 2.405-1.228.92 0 1.662.324 2.228.955.549.631.822 1.484.822 2.558v5.253z"/>
            </svg>
            '''

linkedinSVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-linkedin"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
'''

instagramSVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-instagram"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
'''

# Make button
switch_theme_btn_html = '''
<button id="btn" onclick="setTheme()">THEME</button>
'''
switch_theme_btn_js = ""

with open('js/theming.js', 'r') as file:
    switch_theme_btn_js += "<script>"
    switch_theme_btn_js += ''.join(file.readlines())
    switch_theme_btn_js += "</script>"

with open('../profile.json', 'r') as file:
    profile = json.loads(''.join(file.readlines()))

for blog in profile["blogs"]:
    isSeries = False
    try:
        series = blog["series"]
        isSeries = True
        blogs.append("<details>")
        blogs.append("<summary>"+blog["name"]+"</summary>")
        for chapter in series:
            name = chapter["name"]
            link = chapter["link"]
            isDisabled = False
            try:
                isDisabled = chapter["disabled"]
            except:
                x = 0
            if isDisabled == True:
                blogs.append("<a class='disabled' href='"+link[:-3]+".html"+"'> <li>"+"<s>"+name+"</s>"+"</li></a>")
            else:
                blogs.append("<a href='"+link[:-3]+".html"+"'> <li>"+name+"</li></a>")
        blogs.append("</details>")
    except:
        x = 0

    if isSeries == False:
        name = blog["name"]
        link = blog["link"]
        isDisabled = False
        try:
            isDisabled = blog["disabled"]
        except:
            x = 0
        if isDisabled == True:
            blogs.append("<a class='disabled' href='"+link[:-3]+".html"+"'> <li>"+"<s>"+name+"</s>"+"</li></a>")
        else:
            blogs.append("<a href='"+link[:-3]+".html"+"'> <li>"+name+"</li></a>")

# Contacts icons

try:
    contacts.append("<a href='"+profile["github"]+"'>"+githubSVG+"</a>")
except:
    print("-> Github account skipped")

try:
    contacts.append("<a href='"+profile["twitter"]+"'>"+twitterSVG+"</a>")
except:
    print("-> Twitter account skipped")

try:
    contacts.append("<a rel=\"me\" href='"+profile["mastodon"]+"'>"+mastodonSVG+"</a>")
except:
    print("-> Mastodon account skipped")

try:
    contacts.append("<a href='mailto: "+profile["mail"]+"'>"+mailSVG+"</a>")
except:
    print("-> Mail skipped")

try:
    contacts.append("<a href='"+profile["instagram"]+"'>"+instagramSVG+"</a>")
except:
    print("-> Instagram skipped")

try:
    contacts.append("<a href='"+profile["linkedin"]+"'>"+linkedinSVG+"</a>")
except:
    print("-> Linkedin skipped")

contact = ""
if(len(contacts)!=0):
    contact = '<br><h2>CONTACTS</h2><hr><div class="contact">'+''.join(contacts) + '</div>'

copyright = ""
try:
    copyright = "<footer>"+profile["copyright"]+"</footer>"
except:
    print("-> copyright skipped")

analytics = ""
try:
    analytics = profile["analytics"]
except:
    print("-> Analytics skipped")

indexHTML = [
    '''<!DOCTYPE html><html><head><meta charset="utf-8">
    <link rel="stylesheet" href="index.css"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>''', profile["name"], '''</title></head>
    <body>
    <div class="contents">
    <h1 style="display: inline-block; padding-right: 20px;">''', profile["name"], '''</h1>''',
    switch_theme_btn_html,
    '''<hr>
    <div class="profile">
        <img src="''', profile["profile_picture"], '''"
            width="150" height="150" style="float:left; margin-right: 15px; margin-top: 5px;">
        <p>''','<br>'.join(profile["description"]),'''</p>
        <br>
    </div>
    <h2>BLOGS</h2><hr>
    <div class="project">
        <ul>''', ''.join(blogs), '''</ul>
    </div>''',
    contact,
    '''</div>''',
    copyright, switch_theme_btn_js, analytics, '''
    </body>
    </html>
    '''
]

# Clean build docs
remove_dir("../docs")
create_dir("../docs")

with open('../docs/index.html', 'w') as file:
    file.writelines(indexHTML)


def get_home_button(file_name):
    return "<a class='home' href="+((len(file_name.split('/')) - 1) * '../')+"index.html"+">HOME</a>"+switch_theme_btn_html+'''
---

'''

# Copy resources
shutil.copy('../'+profile["profile_picture"], '../docs/'+profile["profile_picture"])
shutil.copy('css/blog.css', '../docs/blog.css')
shutil.copy('css/index.css', '../docs/index.css')
shutil.copy('js/highlight.min.js', '../docs/highlight.min.js')

# Clean build assets
remove_dir("../docs/assets")
create_dir("../docs/assets")

with os.scandir('../blogs/assets/') as assets:
    for asset in assets:
        asset_ext = os.path.splitext(asset)[1]
        if (asset_ext == ".png" or asset_ext == ".jpeg" or asset_ext == ".mp4" or asset_ext == ".mov"):
            shutil.copy('../blogs/assets/'+asset.name, '../docs/assets/'+asset.name)

def md_to_html(title, file_name):
    process = Popen([
            path_to_pandoc,
            '--metadata', 'title='+title,
            '-s', '--no-highlight',
            '-c', ((len(file_name.split('/')) - 1) * '../') + 'blog.css',
            '../docs/'+file_name,
            '-o', '../docs/'+file_name[:-3]+'.html'
        ], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    error = bytes.decode(stderr)
    if(error == ""):
        print('\033[32m '+file_name+' successfully translated to html'+' \033[0m')
    else:
        print("\033[31m '"+error+"' \033[0m")

def create_blog(title, file_name, dir_name):
    blogContents = []
    blogContents.append('<h1>' + profile["name"] + "</h1>")
    blogContents.append('<div class="contents">')
    blogContents.append(get_home_button(file_name))
    with open('../blogs/' + file_name, 'r') as file:
        blogContents.append(''.join(file.readlines()))
    blogContents.append("\n")
    blogContents.append('\n<script src="' + ((len(file_name.split('/')) - 1) * '../') +'highlight.min.js"></script><script>hljs.highlightAll();</script>')
    blogContents.append(switch_theme_btn_js)
    blogContents.append(analytics)
    blogContents.append('</div>')
    blogContents.append(copyright)
    if(dir_name != ""):
        create_dir('../docs/'+dir_name)
    with open('../docs/' + file_name, 'w') as file:
        file.writelines(blogContents)
    md_to_html(title, file_name)
    os.remove('../docs/' + file_name)

for blog in profile["blogs"]:
    isSeries = False
    try:
        series = blog["series"]
        isSeries = True
        for chapter in series:
            title = chapter["name"]
            file_name = chapter["link"]
            create_blog(title, file_name, file_name.split('/')[0])
    except:
        x = 0

    if isSeries == False:
        title = blog["name"]
        file_name = blog["link"]
        create_blog(title, file_name, "")
