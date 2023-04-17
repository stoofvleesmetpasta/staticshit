import yaml
import markdown
import jinja2
import os

#environment loader
template_loader = jinja2.FileSystemLoader(searchpath='./templates/')
template_env = jinja2.Environment(loader=template_loader)



def addtopostspage(filename):
    source = open("_site/posts/postspage.html", "r")
    postscontent = source.readlines()

    invoegpunt = 12
    postscontent.insert(invoegpunt, f'\t\t<li><a href="{filename}.html">{filename}</a></li>\n')

    destination = open("_site/posts/postspage.html", "w")
    destination.writelines(postscontent)

def addtopagespage(filename):
    source = open("_site/pages/pagespage.html", "r")
    pagescontent = source.readlines()

    invoegpunt = 12
    pagescontent.insert(invoegpunt, f'\t\t<li><a href="{filename}.html">{filename}</a></li>\n')

    destination = open("_site/pages/pagespage.html", "w")
    destination.writelines(pagescontent)

def addfiletosite(filepath, templatetype, uploadpath, filename):

    #markdown bestand openen
    file = open(filepath, "r")
    markdowntext = file.read()

    #checken of er al YAML is door te checken of html file bestaat
    if os.path.exists(uploadpath) == False:

        #YAML laten invullen
        print(f"\ngeef de gegevens voor {filename}: ")
        name = input("uw naam: ")
        date = input("geef de datum (dd-mm-yyyy): ")
        title = input("geef titel: ")

        userinfo = {
            'title': title,
            'date': date,
            'author': name
        }

        #frontmatter toevoegen aan markdown file
        frontmatter = yaml.dump(userinfo, default_style="" "", default_flow_style=False )
        updatedmd =  frontmatter + markdowntext
        html = markdown.markdown(updatedmd)
        title = markdown.markdown(title)


        #template kiezen
        tempkeuze = templatetype
        if tempkeuze == "page":
            templatename = "template2.html"
            addtopagespage(filename)
        elif tempkeuze == "post":
            templatename = "template1.html"
            addtopostspage(filename)

        #parsen naar html
        template = template_env.get_template(templatename)

        renderedhtml = template.render(content=html, title=title)

        file = open(uploadpath, "w")
        file.write(renderedhtml)


for i in os.scandir("posts"):
    filepath = i.path
    uploadpath = "_site/posts/" + i.name[:-2] + "html"
    templatetype = "post"
    filename = i.name[:-3]
    addfiletosite(filepath, templatetype, uploadpath, filename)

for i in os.scandir("pages"):
    filepath = i.path
    uploadpath = "_site/pages/" + i.name[:-2] + "html"
    templatetype = "page"
    filename = i.name[:-3]
    addfiletosite(filepath, templatetype, uploadpath, filename)