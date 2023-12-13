# Data structure
class Blog:
    title = ""
    link = ""
    disabled = False
    
    def __init__(self, title, link, disabled):
        self.title = title
        self.link = link
        self.disabled = disabled

class Contact:
    title = ""
    svg = ""
    link = ""

    def __init__(self, title, svg, link):
        self.title = title
        self.svg = svg
        self.link = link

# Landing Page
name = ""
description = ""
picture = ""
blogs = []
contacts = []
copyright = ""
analytics = ""

profile_html = ""
blogs_html= ""
contacts_html = ""

def set_name(profile_name):
    name = profile_name

def set_description(profile_description):
    description = profile_description

def set_profile_picture(profile_picture):
    picture = profile_picture

def add_blog(blog):
    blogs.append(blog)

def add_contact(contact):
    contacts.append(contact)

def generate_blogs_html():
    tmp_blogs = []
    for blog in blogs:
#    try:
#        series = blog["series"]
#        isSeries = True
#        blogs.append("<details>")
#        blogs.append("<summary>"+blog["name"]+"</summary>")
#        for chapter in series:
#            name = chapter["name"]
#            link = chapter["link"]
#            isDisabled = False
#            try:
#                isDisabled = chapter["disabled"]
#            except:
#                x = 0
#            if isDisabled == True:
#                blogs.append("<a class='disabled' href='"+link[:-3]+".html"+"'> <li>"+"<s>"+name+"</s>"+"</li></a>")
#            else:
#                blogs.append("<a href='"+link[:-3]+".html"+"'> <li>"+name+"</li></a>")
#        blogs.append("</details>")
#    except:
#        x = 0

        name = blog.name
        link = blog.link
        if blog.disabled == True:
            tmp_blogs.append("<a class='disabled' href='"+blog.link[:-3]+".html"+"'> <li>"+"<s>"+blog.title+"</s>"+"</li></a>")
        else:
            tmp_blogs.append("<a href='"+blog.link[:-3]+".html"+"'> <li>"+blog.title+"</li></a>")
    blogs_html = ''.join(tmp_blogs)

def generate_landing():
    generate_blogs_html()
    switch_theme_btn_html = "<button id='btn' onclick='setTheme()'>THEME</button>"
    switch_theme_btn_js = ""
    with open('js/theming.js', 'r') as file:
        switch_theme_btn_js += "<script>"
        switch_theme_btn_js += ''.join(file.readlines())
        switch_theme_btn_js += "</script>"

    profile_html = ''.join([
    '''<h1 style="display: inline-block; padding-right: 20px;">''', name, '''</h1>''',
        switch_theme_btn_html,
        '''<hr>
        <div class="profile">
            <img src="''', profile_picture, '''"width="150" height="150" style="float:left; margin-right: 15px; margin-top: 5px;">
            <p>''', description ,'''</p>
            <br>
        </div>'''])
    final_blogs_html = ''.join([
    '''<h2>BLOGS</h2><hr>
        <div class="project">
            <ul>''', blogs_html, '''</ul>
        </div>'''
        ])
    contacts_html = ''.join([
        contact,
        '''</div>''',
        copyright, switch_theme_btn_js, analytics
    ])

    final_html = ''.join([
    '''<!DOCTYPE html><html><head><meta charset="utf-8">
    <link rel="stylesheet" href="index.css"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>''', profile["name"], '''</title></head>
    <body>''',
    profile_html,
    final_blogs_html,
    contacts_html,
    '''
    </body>
    </html>
    '''
    ])



