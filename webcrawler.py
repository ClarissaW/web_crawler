from bs4 import BeautifulSoup
import requests
import pdfkit
import os

"""Parse the content of each page"""
def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    header = soup.findAll('div',{"class" : "hero-unit"})[0]
    title_author(header)
    return response.text


"""Get the title and the author of this page, but this will not be used for here"""
def title_author(content):
    title = content.findAll('h1')[0]
    author = content.findAll('h2', {"class", "author"})[0]
    return title,author


"""Get all the urls from the main page, and transfer the urls to the function parse_page"""
def parse_url(start_url):
    urls = []
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text,"html.parser")
    for link in soup.find_all('div',{"id":"fh-chapters-list"}):
        extensions = link.find_all('a')
        for extension in extensions:
            href = "http://www.aosabook.org/en/" + extension.get('href')
            urls.append(href)
    return urls


"""Write the content to different htmls"""
def write_content_to_html(urls):
    htmls=[]
    for url in urls:
        content = parse_page(url)
        print(url)
        f_name = url[32:]
        with open(f_name,"w+") as f:
            f.write(content)
        htmls.append(f_name)
    return htmls


"""A little frustrated because i don't know why i cannot transfer all the htmls into one pdf file and delete the html file. sometimes get warning(taking too long to load)"""
#transfer each html into pdf,pay attention to the path of wkhtmltopdf, when it cannot be found out, the path could be specified.
def htmlToPdf_removeHtmls(htmls):
    WKHTMLTOPDF_PATH = '/usr/local/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    for html in htmls:
        pdfkit.from_file(html, html + '.pdf', configuration = config, options = options)
        os.remove(html)

"""Format option: dpi could be used for manually changing the font size """
options = {
    'dpi':1000,
    'page-size': 'Letter',
#    'margin-top': '0.75in',
#    'margin-right': '0.75in',
#    'margin-bottom': '0.75in',
#    'margin-left': '0.75in',
     'encoding': "UTF-8"
#    'custom-header': [
#        ('Accept-Encoding', 'gzip')
#    ],
#    'cookie': [
#        ('cookie-name1', 'cookie-value1'),
#        ('cookie-name2', 'cookie-value2'),
#    ],
#    'outline-depth': 10,
}


start_url = "http://www.aosabook.org/en/index.html"
urls = parse_url(start_url)
htmls = write_content_to_html(urls)
htmlToPdf_removeHtmls(htmls)

"""two ways to find_all"""
#soup.find_all("div", class_="stylelistrow")
#mydivs = soup.findAll("div", { "class" : "stylelistrow" })


"""could crawl particular information from this website, this is just an example"""
#    for para in soup.findAll('p'):
#        if para.findAll('em'):
#            em = para.findAll('em')
#            print(em)
#        elif para.findAll('pre',{"class" : "sourceCode python"}):
#            for code in para.findAll('code',{"class" : "sourceCode python"}):
#                code_text = code.findAll('span')
#                print(code_text)
#        else:
#            print(para)

"""html files could be like this"""
#text = """
#    <html>
#    <head>
#    <title >hello, world</title>
#    </head>
#    <body>
#    <h1>BeautifulSoup</h1>
#    <p class="bold">如何使用BeautifulSoup</p>
#    <p class="big" id="key1"> 第二个p标签</p>
#    <a href="http://foofish.net">python</a>
#    </body>
#    </html>
#    """

"""directly find out something from the label"""
#print(soup.title)


