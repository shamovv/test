# -*- coding: utf-8 -*-
from flask import Flask, request, make_response, jsonify
import sqlite3
import random
conn = sqlite3.connect("materials.db", check_same_thread=False)
cursor = conn.cursor()


app = Flask(__name__)

@app.route('/')
def all():
    cursor.execute("SELECT * FROM Links")
    data = cursor.fetchall()

    page = "<table>"
    for row in data:
        page += "<tr>"
        for column in row:
            page += "<td>" + str(column) + "</td>"
        page += "</tr>"
    page += "</table>"

    return page


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        sphere = request.form['sphere']
        level = request.form['level']
        tip = request.form['tip']
        link = request.form['link']

        cursor.execute(f"INSERT INTO Links(sphere, level, type, link) VALUES ('{sphere}', '{level}', '{tip}', '{link}')")
        conn.commit()
        return "Added!"
    else:
        page = '''
        <form method="post">
            <label>Сфера</label> <br>
            <input type='text' name='sphere'></input> <br> 
            <label>Уровень</label> <br>
            <input type='text' name='level'></input> <br>
            <label>Тип</label> <br>
            <input type='text' name='tip'></input> <br>
            <label>Ссылка</label> <br>
            <input type='text' name='link'></input> <br>
    
            <input type='submit'>
        </form>
        '''
        return page


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == "POST":
        material_id = request.form['id']

        cursor.execute(f"DELETE FROM Links WHERE id={material_id}")
        conn.commit()
        return "Deleted!"
    else:
        page = '''
        <form method="post">
            <label>Удалить материал</label> <br>
            <input type='number' name='id'></input> <br> 

            <input type='submit'>
        </form>
        '''
        return page


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    
    action = req.get('queryResult').get('action')
    

    if action == 'get_material':
        sphr = req.get('queryResult').get('parameters').get('sphere')
        lvl = req.get('queryResult').get('parameters').get('level')
        res = get_material(sphr, lvl) 
    elif action == 'motivation':
        res = get_motivation()
    else:
        res = 'hi'

    print('Action: ' + action)
    print('Response: ' + res)

    return make_response(jsonify({'fulfillmentText': res}))

def get_motivation():
    s = ['Давай!', 'Вперед!', 'Ты сможешь', 'Не унывай']
    #res = random.choice(s)
    res = s[random.randint(0, len(s))]
    return res

def get_material(s, lvl, t="-"):
    if t == "-":
        sql = f"SELECT link FROM Links WHERE sphere='{s}' AND level='{lvl}'"
    else:
        sql = f"SELECT link FROM Links WHERE sphere='{s}' AND level='{lvl}' AND type='{t}'"
    cursor.execute(sql)
    if cursor.fetchone() == None:
        card = "К сожалению, в базе нет такого материала!"
    else:
        res = cursor.fetchone()[0]
        card = f"Вот материал по теме {s} уровня {lvl}: {res}"
    return card



if __name__ == '__main__':
    app.run(debug=True)













