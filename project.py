import markdown2
import os
import re
from validator_collection import validators, checkers, errors
import http.server
import socketserver


# server parameters
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

# global variables
style = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous"><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>'
header = "<html><head>" + style + "</head><body>"
nav = '<nav class="navbar bg-dark"><div class="container"><a class="navbar-brand" href="index.html"><img src="pynt.png" /></a><nav class="nav"><a class="nav-link active text-white" aria-current="page" href="index.html">Home</a><a class="nav-link text-white" href="about.html">About</a><a class="nav-link text-white" href="contact.html">Contact</a></a></nav></div></nav><div class="container"><div class="row"><div class="column"><br />'
footer = "</div></div></div></body></html>"
markdown_docs_list = os.listdir('md/')

def main():
    # create html files (posts and pages)
    for item in markdown_docs_list:
        md_file_content = extract_md_content(item)
        create_html_files(md_file_content, item)
    
    # create index.html (blog post list) page
    links = []
    for item in markdown_docs_list:
        if build_post_links(item):
            links.append(build_post_links(item))
    links.sort(key = lambda x: re.search(".*(\d\d\d\d-\d\d-\d\d).*", x).group(1), reverse=True)
    links_html = "".join(links)
    
    build_index_page(links_html)
    
    run_server()


def extract_md_content(file_name):
    try:
        with open(f"md/{file_name}", "r") as file:
            lines = file.readlines()
            validate_docs(lines)
            lines = lines[1:]
            return "".join(lines)
    except FileNotFoundError:
        return f"File does not exist"
            

def create_html_files(md_text, full_file_name):            
    html_text = header + nav + markdown2.markdown(md_text) + footer
    f = open(f"./html/{full_file_name.split('.')[0]}.html", "w")
    f.write(html_text)
    f.close
    return


def build_post_links(file_name):
    f = open(f"md/{file_name}", "r")
    lines = f.readlines()
    if lines[0] == 'post\n':
        matches = re.search("^#(.+)\n$", lines[2])
        title = matches.group(1)
        return f"<li><a href='{file_name.split('.')[0]}.html'>{title}</a> - <span class='date'>{lines[1]}</span></li>"


def build_index_page(links_html):
    index_html = header + nav + '<h1>Latest Entries</h1>' + '<ul>' + links_html + '</ul>' + footer
    f = open(f"./html/index.html", "w")
    f.write(index_html)
    f.close
    return


def validate_docs(a_list):
    if a_list[0] == 'post\n':
        match = re.search("([^\n]+)", a_list[1])
        if validate_date(match[1]) == "Valid":
            return
        else:
            raise ValueError("Invalid Date in one of your posts")
    elif a_list[0] == 'page\n':
        return
    else:
        raise ValueError("A file can only be labelled as a post or page, lowercase letters")
    

def validate_date(post_date):
    try:
        validators.date(post_date)
        return "Valid"
    except ValueError:
        return "Invalid Date"


def run_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        print(f"Follow this link: http://localhost:{PORT}/html")
        httpd.serve_forever()


if __name__ == "__main__":
    main()