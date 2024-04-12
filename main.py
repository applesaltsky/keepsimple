#uvicorn main:app --reload -> on window
#gunicorn -w main:app -> on linux

from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from IndexConnector import IndexConnector


MAIN_PY_PATH = Path(__file__)
TEMPLATES_PATH = Path(MAIN_PY_PATH.parent,'templates')

app = FastAPI()
env = Environment(loader = FileSystemLoader(TEMPLATES_PATH), autoescape=select_autoescape())
index_db = IndexConnector()
index_db.refresh()

@app.get("/")
def root():
    return RedirectResponse('/0/0')


@app.get("/{a:int}/{b:int}")
def render(a,b):
    #get templates index from db
    index = index_db.read_row(id_category=a,id_content=b)  #{'id': 3, 'id_category': 1, 'category': '이 앱은 어떻게 만들었나', 'id_content': 2, 'title_content': 'JINJA2를 이용한 RENDERING', 'html_content': 'Jinja2.html'}
    id_category = index['id_category']
    category = index['category']
    id_content = index['id_content']
    title_content = index['title_content']
    html_content = index['html_content']


    #get category list
    list_id_category, list_category = index_db.get_list_category()

    #get title list
    list_id_content, list_title_content, list_html_content = index_db.get_list_content(id_category)

    templates = env.get_template(f'content/{id_category}_{category}/{id_content}_{title_content}/{html_content}')
    text = templates.render({
                            'list_id_category':list_id_category,
                             'list_category':list_category,
                             'list_id_content':list_id_content,
                             'list_title_content':list_title_content,
                             'title':title_content,
                             'this_id_category':id_category,
                             'zip':zip,
                             'enumerate':enumerate
                             })

    
    headers = {'Content-type':'text/html'}
    return Response(text,status_code=200,headers=headers)
