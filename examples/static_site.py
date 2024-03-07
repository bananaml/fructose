# This examples demonstrates how to use Fructose to generate fake data while following a strict schema.

from fructose import Fructose
from http.server import BaseHTTPRequestHandler, HTTPServer


# Create a new instance of the Fructose
ai = Fructose()

header = """
 ____  ____  _  _   ___  ____  __   ____  ____ 
(  __)(  _ \/ )( \ / __)(_  _)/  \ / ___)(  __)
 ) _)  )   /) \/ (( (__   )( (  O )\___ \ ) _) 
(__)  (__\_)\____/ \___) (__) \__/ (____/(____)
"""

# decorate your function to call an LLM. Your ways to guide the LLM are through the docstring,
# functions parameters & arguments and the return type.
@ai()
def generate_static_site() -> str:
    """
    Generate valid HTML for a static site.
    
    Contents: 
    The name of the site (Fructose) in a very large sans serif font.
    The tagline of the site should be "LLM calls as strongly-typed functions".
    There should be call to action button which links to https://github.com/bananaml/fructose to star the project.

    Style:
    The background should be a light gradient. Every section be centered. The page as large as the
    viewport. Boxes should have rounded corners. The site should be professional and modern. 
    """
    ...

def create_handler(html_content):
    class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
    
    return CustomHTTPRequestHandler

def run(html_content, server_class=HTTPServer, port=8000):

    handler_class = create_handler(html_content)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print(header) 
    print(f'Go to http://localhost:{port}/')
    print(f'Press Ctrl+C to stop the server \n')
    print(f'------------------------ \n')  
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print('Stopping httpd...\nHTTP server stopped.')

def main():
    html = generate_static_site()
    run(html)

if __name__ == "__main__":
    main()


