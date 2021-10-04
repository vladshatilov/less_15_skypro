from flask import Flask, render_template, request
import sqlite3
from query_templates import query_create_animals_index_table, query_create_breed_index_table, \
    query_create_colors_index_table, search_db, get_len_db


def alter_db(query):
    conn = sqlite3.connect('animal.db')
    curs = conn.cursor()
    curs.executescript(query)
    curs.close()


app = Flask(__name__)


@app.route('/')
def hello_world():
    query_list = [query_create_breed_index_table,query_create_colors_index_table,query_create_animals_index_table]
    for query in query_list:
        alter_db(query)
    len_num = get_len_db()[0]['len_num']
    print(len_num)
    return render_template('index.html',len_num=len_num)

@app.route('/<int:animal_id>')
def profile(animal_id):
    animal = search_db(animal_id)[0]
    print(animal)
    return render_template('animal_page.html',animal_item=animal)


if __name__ == '__main__':
    app.run()
