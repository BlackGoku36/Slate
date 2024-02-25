import os
import shutil
import sys
from subprocess import Popen, PIPE

# SVGs

mailSVG = """<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-mail">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
            </svg>"""
twitterSVG = """<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-twitter">
                <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z">
                </path>
            </svg>"""
githubSVG = """<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-github">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22">
                </path>
            </svg>"""

mastodonSVG = """
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21.327 8.566c0-4.339-2.843-5.61-2.843-5.61-1.433-.658-3.894-.935-6.451-.956h-.063c-2.557.021-5.016.298-6.45.956 0 0-2.843 1.272-2.843 5.61 0 .993-.019 2.181.012 3.441.103 4.243.778 8.425 4.701 9.463 1.809.479 3.362.579 4.612.51 2.268-.126 3.541-.809 3.541-.809l-.075-1.646s-1.621.511-3.441.449c-1.804-.062-3.707-.194-3.999-2.409a4.523 4.523 0 0 1-.04-.621s1.77.433 4.014.536c1.372.063 2.658-.08 3.965-.236 2.506-.299 4.688-1.843 4.962-3.254.434-2.223.398-5.424.398-5.424zm-3.353 5.59h-2.081V9.057c0-1.075-.452-1.62-1.357-1.62-1 0-1.501.647-1.501 1.927v2.791h-2.069V9.364c0-1.28-.501-1.927-1.502-1.927-.905 0-1.357.546-1.357 1.62v5.099H6.026V8.903c0-1.074.273-1.927.823-2.558.566-.631 1.307-.955 2.228-.955 1.065 0 1.872.409 2.405 1.228l.518.869.519-.869c.533-.819 1.34-1.228 2.405-1.228.92 0 1.662.324 2.228.955.549.631.822 1.484.822 2.558v5.253z"/>
            </svg>
            """

linkedinSVG = """<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-linkedin"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
"""

instagramSVG = """<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-instagram"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
"""

path_to_pandoc = 'pandoc'
try:
    path_to_pandoc = sys.argv[1]
except:
    print('Trying installed pandoc at PATH')


# Data structure
class Site:
    name = ""
    description = ""
    picture = ""
    blogs = []
    contacts = []
    copyright = ""
    analytics_html = ""

class Blog:
    title = ""
    link = ""
    disabled = False

    def __init__(self, title, link, disabled):
        self.title = title
        self.link = link
        self.disabled = disabled

class Series:
    title = ""
    blogs = []

    def __init__(self, title, blogs):
        self.title = title
        self.blogs = blogs

class Contact:
    svg = ""
    link = ""
    is_mail = False

    def __init__(self, svg, link, is_mail):
        self.svg = svg
        self.link = link
        self.is_mail = is_mail

    def twitter(link):
        return Contact(twitterSVG, link, False)

    def github(link):
        return Contact(githubSVG, link, False)

    def mastodon(link):
        return Contact(mastodonSVG, link, False)

    def linkedin(link):
        return Contact(linkedinSVG, link, False)

    def instagram(link):
        return Contact(instagramSVG, link, False)

    def mail(link):
         return Contact(mailSVG, link, True)

profile_html = ""
blogs_html = ""
contacts_html = ""

def get_docs_path():
    return os.getcwd() + '/docs'

def get_blogs_path():
    return os.getcwd() + '/blogs'

def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

def copy_assets(site):
    shutil.copy(get_script_path() + '/css/blog.css', get_docs_path() + '/blog.css')
    shutil.copy(get_script_path() + '/css/index.css', get_docs_path() + '/index.css')
    shutil.copy(get_script_path() + '/js/highlight.min.js', get_docs_path() + '/highlight.min.js')
    shutil.copy(os.getcwd() + '/' + site.picture, get_docs_path() + '/' + site.picture)

def generate_blogs_html(site):
    global blogs_html
    tmp_blogs = []
    for blog in site.blogs:
        if(type(blog) == Series):
            tmp_blogs.append("<details>")
            tmp_blogs.append("<summary>"+blog.title+"</summary>")
            for chapter in blog.blogs:
                if chapter.disabled == True:
                    tmp_blogs.append("<a class='disabled' href='"+chapter.link[:-3]+".html"+"'> <li>"+"<s>"+chapter.title+"</s>"+"</li></a>")
                else:
                    tmp_blogs.append("<a href='"+chapter.link[:-3]+".html"+"'> <li>"+chapter.title+"</li></a>")
            tmp_blogs.append("</details>")
        else:
            if blog.disabled == True:
                tmp_blogs.append("<a class='disabled' href='"+blog.link[:-3]+".html"+"'> <li>"+"<s>"+blog.title+"</s>"+"</li></a>")
            else:
                tmp_blogs.append("<a href='"+blog.link[:-3]+".html"+"'> <li>"+blog.title+"</li></a>")
    blogs_html = ''.join(tmp_blogs)

def generate_contacts_html(site):
    global contacts_html
    tmp_contacts = []
    for contact in site.contacts:
        if(contact.is_mail == True):
            tmp_contacts.append("<a href='mailto: "+contact.link+"'>"+contact.svg+"</a>")
        else:
            tmp_contacts.append("<a href='"+contact.link+"'>"+contact.svg+"</a>")

    contacts_html = '<br><h2>CONTACTS</h2><hr><div class="contact">' + ''.join(tmp_contacts) + '</div>'

def md_to_html(title, file_name):
    process = Popen([
            path_to_pandoc,
            '--metadata', 'title='+title,
            '-s', '--no-highlight',
            '-c', ((len(file_name.split('/')) - 1) * '../') + 'blog.css',
            get_docs_path() + '/' + file_name,
            '-o', get_docs_path() + '/' + file_name[:-3]+'.html'
        ], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    error = bytes.decode(stderr)
    if(error == ""):
        print('\033[32m '+file_name+' successfully translated to html'+' \033[0m')
    else:
        print("\033[31m '"+error+"' \033[0m")

switch_theme_btn_html = '''
<button id='btn' onclick='setTheme()'>THEME</button>
'''

def get_home_button(file_name):
    return "<a class='home' href="+((len(file_name.split('/')) - 1) * '../')+"index.html"+">HOME</a>"+switch_theme_btn_html+'''
---

'''

def create_blog(site, blog):
    path_to_input_blog = get_blogs_path() + '/' + blog.link
    path_to_output_blog = get_docs_path() + '/' + '/'.join(blog.link.split('/')[:-1])
    print(path_to_output_blog)
    if(os.path.exists(path_to_input_blog) == False):
        print("Path to the input blog directory doesn't exists, please make sure it exists, Path: {" + path_to_input_blog + "}")
        return
    os.makedirs(path_to_output_blog, exist_ok=True)

    switch_theme_btn_js = ""
    with open('Slate/js/theming.js', 'r') as file:
        switch_theme_btn_js += "<script>"
        switch_theme_btn_js += ''.join(file.readlines())
        switch_theme_btn_js += "</script>"

    blogContents = []
    blogContents.append('<h1>' + site.name + "</h1>")
    blogContents.append('<div class="contents">')
    blogContents.append(get_home_button(blog.link))
    with open(get_blogs_path() + '/' + blog.link, 'r') as file:
        blogContents.append(''.join(file.readlines()))
    blogContents.append("\n")
    blogContents.append('\n<script src="' + ((len(blog.link.split('/')) - 1) * '../') +'highlight.min.js"></script><script>hljs.highlightAll();</script>')
    blogContents.append(switch_theme_btn_js)
    blogContents.append(site.analytics_html)
    blogContents.append('</div>')
    blogContents.append('<footer>' + site.copyright + '</footer>')
    dir_name = blog.link.split('/')[0]
    with open(get_docs_path() + '/' + blog.link, 'w') as file:
        file.writelines(blogContents)
    md_to_html(blog.title, blog.link)
    os.remove(get_docs_path() + '/' + blog.link)

def generate_blogs(site):
    for blog in site.blogs:
        if(type(blog) == Series):
            for chapter in blog.blogs:
                create_blog(site, chapter)
        else:
            create_blog(site, blog)

def generate_landing(site):
    switch_theme_btn_js = ""
    with open('Slate/js/theming.js', 'r') as file:
        switch_theme_btn_js += "<script>"
        switch_theme_btn_js += ''.join(file.readlines())
        switch_theme_btn_js += "</script>"

    profile_html = ''.join([
    '''<h1 style="display: inline-block; padding-right: 20px;">''', site.name, '''</h1>''',
        switch_theme_btn_html,
        '''<hr>
        <div class="profile">
            <img src="''', site.picture, '''"width="150" height="150" style="float:left; margin-right: 15px; margin-top: 5px;">
            <p>''', site.description ,'''</p>
            <br>
        </div>'''])
    final_blogs_html = ''.join([
    '''<h2>BLOGS</h2><hr>
        <div class="project">
            <ul>''', blogs_html, '''</ul>
        </div>'''
        ])
    final_html = ''.join([
    '''<!DOCTYPE html><html><head><meta charset="utf-8">
    <link rel="stylesheet" href="index.css"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>''', site.name, '''</title></head>
    <body>
    <div class="contents">
    ''',
    profile_html,
    final_blogs_html,
    contacts_html,
    '''</div>''',
    '''<footer>''', site.copyright, '''</footer>''',
    switch_theme_btn_js,
    site.analytics_html,
    '''
    </body>
    </html>
    '''
    ])
    with open(get_docs_path() + '/index.html', 'w') as file:
        file.write(final_html)

def generate_site(site):
    # TODO: Create these error more descriptive, maybe say why you need to create those folders
    if(os.path.isdir(get_docs_path()) != True):
        print("docs folder not found, please create folder named 'docs'")
        return
    if(os.path.isdir(get_blogs_path()) != True):
        print("blogs folder not found, please create folder named 'blogs'")
        return
    generate_blogs(site)
    generate_contacts_html(site)
    generate_blogs_html(site)
    generate_landing(site)
    copy_assets(site)
