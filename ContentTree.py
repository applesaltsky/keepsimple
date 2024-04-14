import os
from pathlib import Path

PATH_CONTENTTREE_PY = Path(__file__)
PATH_CONTENT = Path(PATH_CONTENTTREE_PY.parent,'templates','content')


class ContentTree:
    def __init__(self):
        self.path_content = PATH_CONTENT
        self.columns = {'id':int, 'id_category':int, 'category':str, 'id_content':int, 'title_content':str, 'html_content':str}
        self.defaultRow = {'id':0, 'id_category':0, 'category':'-', 'id_content':0, 'title_content':'-', 'html_content':'-'}

    def get_tree(self):
        rst = []
        id = 0

        list_category = os.listdir(self.path_content)
        list_category.sort(key=lambda item:item.split('_')[0])
        for category in list_category:
            path_category = Path(self.path_content,category)
            list_content = os.listdir(path_category)
            list_content.sort(key=lambda item:item.split('_')[0])
            for title in list_content:
                path_content = Path(self.path_content,category,title)
                html_content = os.listdir(path_content)[0]
                newRow = {'id':int(id), 
                          'id_category':int(category.split('_')[0]), 
                          'category':category.split('_')[1], 
                          'id_content':int(title.split('_')[0]),  
                          'title_content':title.split('_')[1], 
                          'html_content':html_content}
                id += 1
                rst.append(newRow)
        return rst

#for i in ContentTree().get_tree():
#    print(i)

'''
{'id': 0, 'id_category': 0, 'category': 'intro', 'id_content': 0, 'title_content': 'hello', 'html_content': 'hello_world.html'}
{'id': 1, 'id_category': 1, 'category': '이 앱은 어떻게 만들었나', 'id_content': 0, 'title_content': '구조', 'html_content': 'structure.html'}
{'id': 2, 'id_category': 1, 'category': '이 앱은 어떻게 만들었나', 'id_content': 1, 'title_content': 'HTTP와 FASTAPI', 'html_content': 'fastapi.html'}
{'id': 3, 'id_category': 1, 'category': '이 앱은 어떻게 만들었나', 'id_content': 2, 'title_content': 'JINJA2를 이용한 RENDERING', 'html_content': 'Jinja2.html'}
{'id': 4, 'id_category': 1, 'category': '이 앱은 어떻게 만들었나', 'id_content': 3, 'title_content': 'SQLITE3', 'html_content': 'sqlite3.html'}
{'id': 5, 'id_category': 1, 'category': '이 앱은 어떻게 만들었나', 'id_content': 4, 'title_content': 'AZURE를 이용한 배포', 'html_content': 'azure.html'}
'''