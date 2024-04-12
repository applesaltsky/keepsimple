import sqlite3
from pathlib import Path
import os
from ContentTree import ContentTree

INDEXCONNECTOR_PY_PATH = Path(__file__)
INDEX_DB_PATH = Path(INDEXCONNECTOR_PY_PATH.parent,'db','indexTable.db')

class IndexConnector:
    def __init__(self)->None:
        self.path = INDEX_DB_PATH
        self.columns = {'id':int, 'id_category':int, 'category':str, 'id_content':int, 'title_content':str, 'html_content':str}   #deleted 0 : false / 1 : true
        #each id should be positive integer (start from 1)
        self.name = 'IndexTable'
    
        self.default_row = {}  #{'id':99999, 'id_category':99999, 'category':'-', 'id_content':99999, 'title_content':'-', 'html_content':'-'}
        for col,tp in zip(self.columns.keys(),self.columns.values()):
            if tp == int:
                self.default_row[col] = 99999
            elif tp == str:
                self.default_row[col] = '-'
            else:
                continue

    def is_suitable_row(self,row:dict)->bool:
        for col,tp in zip(self.columns.keys(),self.columns.values()): 
            if not col in row:
                return False
            if not type(tp()) == type(row[col]):
                print(col)
                print(type(tp()))
                print(type(row[col]))
                return False
        return True
    
    def is_existent_db(self)->bool:
        return os.path.exists(self.path)
      
    def initial_db(self)->bool:
        if not self.is_existent_db():
            try:
                with sqlite3.connect(self.path) as con:
                    cur = con.cursor()
                    sql = f'''create table if not exists {self.name} 
                                                (id int, 
                                                id_category int, 
                                                category varchar(255),
                                                id_content int,
                                                title_content varchar(255),
                                                html_content varchar(255)                                            
                                                );
                            '''
                    cur.execute(sql)
                return True
            
            except Exception as e:
                print(e)
                con.close()
                if self.is_existent_db():
                    os.remove(self.path)
                return False
        return False
                
    def delete_db(self)->bool:
        if self.is_existent_db():
            try:
                os.remove(self.path)
                return True
            except Exception as e:
                print(e)
                return False
        return False
        
    def read_all(self)->list[dict]:       
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            sql = f'''select * from {self.name}'''
        
        rst = []
        for row in cur.execute(sql):   #change tuple to dict
            row_dict = self.default_row.copy()
            for item,col in zip(row,row_dict):
                row_dict[col]=item
            rst.append(row_dict)
        return rst

    def show_all(self)->list[dict]:     
        rst = self.read_all()  
        for row in rst:
            print(row) 
        return rst
    
    def read_row(self, id_category:int, id_content:int)->tuple:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            sql = f'''select * 
                    from {self.name} 
                    where 1=1
                        and id_category = {id_category} 
                        and id_content = {id_content}
                    '''
            for row in cur.execute(sql):   #change tuple to dict
                row_dict = self.default_row.copy()
                for item,col in zip(row,row_dict):
                    row_dict[col]=item
        return row_dict

    def shape(self)->tuple[int]:
        rst = self.read_all()
        if len(rst) == 0:
            return (0,0)
        else:
            row_cnt = len(rst)
            col_cnt = len(rst[0])
            return (row_cnt,col_cnt)

    def create_one(self,row:dict)->bool:       
        if not self.is_suitable_row(row):
            return False
        
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            sql = f"""insert into {self.name} 
                                    (id, id_category, category, id_content, title_content, html_content) 
                             values (
                                    {row['id']},
                                    {row['id_category']},
                                    '{row['category']}',
                                    {row['id_content']},
                                    '{row['title_content']}',
                                    '{row['html_content']}'
                                    )"""
            cur.execute(sql)   
        return True     
                        
    def delete_one(self,id:int=None,id_category:int=None,id_content:int=None)->bool:       
        try:
            with sqlite3.connect(self.path) as con:
                cur = con.cursor()
                sql = ''

                if id is not None:
                    sql = f"""delete from {self.name} where id = {id};"""

                elif (id_category is not None) and (id_content is not None):
                    sql = f"""delete from {self.name} where id_category = {id_category} and id_content = {id_content};"""

                else:
                    return False

                cur.execute(sql)
            return True
            
        except Exception as e:
            print(e)
            return False
        
    def get_list_category(self)->tuple[list]:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            sql = f"""select distinct id_category, category 
                      from {self.name}"""
            list_id_category = []
            list_category = []
            for id_category,category in cur.execute(sql):
                list_id_category.append(id_category)
                list_category.append(category)
        return (list_id_category, list_category)
    
    def get_list_content(self,id_category:int)->tuple:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            sql = f"""select distinct id_content, title_content, html_content 
                      from {self.name} 
                      where 1=1
                        and id_category = {id_category}
                   """
            list_id_content = []
            list_title_content = []
            list_html_content = []
            for id_content,title_content,html_content in cur.execute(sql):
                list_id_content.append(id_content)
                list_title_content.append(title_content)
                list_html_content.append(html_content)
        return (list_id_content, list_title_content, list_html_content)  

    def refresh(self)->bool:
        self.delete_db()
        self.initial_db()
        for row in ContentTree().get_tree(): 
            self.create_one(row)

    


        

#test code
#index_db = IndexConnector()
#index_db.refresh()
#index_db.show_all()
##print(index_db.read_row(id_category=1,id_content=2))
#index_db.delete_db()
#row = {'id':0, 'id_category':1, 'category':'-', 'id_title':99999, 'title':'-', 'id_content':99999, 'html_content':'-'}
#for row in ContentTree().get_tree():
#    print(row)
#    index_db.create_one(row)

#index_db.create_one(row)
#index_db.show_all()
#print(index_db.get_list_category())
#print(index_db.get_list_content(0))
#print(index_db.columns_str)
#print(index_db.default_row)
