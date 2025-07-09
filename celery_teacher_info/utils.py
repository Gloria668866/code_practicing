from .webcontent import WebContent

def get_html(url):
    web_content = WebContent()
    html = web_content.get_html_via_drission(url)
    return html