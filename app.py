from flask import (Flask, render_template, 
                   request, jsonify,
                   make_response, json,
                   send_file, redirect)
import sqlite3
import pandas as pd
import datetime
import xlsxwriter

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

app= Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    search_term = request.form['searchTerm']
    col = request.form['col']
    table = request.form['table']
    filter = request.form['filter']
    month = request.form['month']
    # Perform database query or any other search logic here
    conn = sqlite3.connect('static/data/data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    if filter=="*" :
        try:
         cur.execute(
            f"SELECT * FROM masters join {table} using(code_no) where {col} like '%{search_term}%'"
            )
        except:
          cur.execute(f"SELECT * FROM masters join {table} using(code_no)")
    elif filter=="M" or filter=="Q":
        try:
         cur.execute(
            f"SELECT * FROM masters join {table} using(code_no) where {col} like '%{search_term}%' and r_type='{filter}'"
            )
        except:
          cur.execute(f"SELECT * FROM masters join {table} using(code_no) where r_type='{filter}'")
    elif filter=="C" or filter=="R":
        try:
         cur.execute(
            f"SELECT * FROM masters join {table} using(code_no) where {col} like '%{search_term}%' and d_type='{filter}'"
            )
        except:
          cur.execute(f"SELECT * FROM masters join {table} using(code_no) where d_type='{filter}'")
    elif filter=="F" or filter=="P" :
        if table != "r9":
            try:
             cur.execute(
                f"SELECT * FROM masters join {table} using(code_no) where {col} like '%{search_term}%' and {month}='{filter}'"
                )
            except:
             cur.execute(f"SELECT * FROM masters join {table} using(code_no) where {month}='{filter}'")
        else:
            try:
             cur.execute(
                f"SELECT * FROM masters join {table} using(code_no) where {col} like '%{search_term}%' and status='{filter}'"
                 )
            except:
             cur.execute(f"SELECT * FROM masters join {table} using(code_no) where status='{filter}'")
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/gstr-1')
def gstr1():
    return render_template('gstr-1.html')


@app.route('/export', methods=["POST", "GET"])
def export():
    return render_template('export.html')

@app.route('/fy')
def fy():
    return render_template('f_y.html', datetime=datetime)

@app.route('/masters', methods=["POST", "GET"])
def masters():
    if request.method == 'POST':
        list=[request.form["File No."],request.form["Name"],
             request.form["Gst_No."], request.form["Working_hand"], 
              request.form["r_type"] , request.form["d_type"],]
        conn=sqlite3.connect("static/data/data.db")
        cur=conn.cursor()
        cur.execute("INSERT into masters (code_no, name, gst_no, working_hand, r_type, d_type) values (?,?,?,?,?,?)",
                    list)
        if list[4] == "Q":
           cur.execute(f"insert into r1 (code_no, Apr, May, Jul, Aug, Oct, Nov, Jan, Feb) values('{list[0]}', 'N','N','N','N','N','N','N','N')")
           cur.execute(f"insert into r3b (code_no , Apr, May, Jul, Aug, Oct, Nov, Jan, Feb) values('{list[0]}','N','N','N','N','N','N','N','N')")   
        elif list[4]=="M":
          cur.execute(f"insert into r1 (code_no) values('{list[0]}')")
          cur.execute(f"insert into r3b (code_no) values('{list[0]}')")
        cur.execute(f"insert into r9 (code_no) values('{list[0]}')")
        conn.commit()
        return redirect('/masters')
    elif request.method == 'GET':
        return render_template('masters.html')

@app.route('/update', methods=["POST", "GET"])
def update():
    if request.method == 'POST':
        codeno=request.form.getlist('code')
        return render_template("update.html", code=codeno)
    elif request.method == 'GET':
        return render_template('detail.html')

@app.route('/submit', methods=["POST", "GET"])
def submit():
    if request.method == 'POST':
        list=[request.form.getlist("code_no",), request.form["month"],request.form["status"],
               ]
        table = request.cookies.get('table')
        conn=sqlite3.connect('static/data/data.db')
        cur=conn.cursor()
        for code in list[0]:
            cur.execute(f"UPDATE {table} SET {list[1]} = '{list[2]}' where code_no = {code}")
            conn.commit()
        return redirect('/gstr-1')
    elif request.method == 'GET':
        return render_template('update.html')
    
# download generated csv or excel
@app.route('/download', methods=["POST", "GET"])
def download():
    file_name=request.form['return']
    conn = sqlite3.connect('static/data/data.db')
    filter = request.form['filter']
    month = request.form['month']
    #cur.execute('SELECT * FROM masters join r1 using(code_no)')
    path = f"static/data/{file_name}.xlsx"

    def to_excel(table):
      with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        try:
            table.to_excel(writer, sheet_name = "Sheet1", header = True, index = False)
            print("File saved successfully!")
        except:
            print("There is an error")
    writer = pd.ExcelWriter(path)
    if filter == '*':
      table = pd.read_sql_query(f"SELECT * FROM masters join {file_name} using(code_no)", conn)
      to_excel(table)
      
    elif filter == 'C' or filter == 'R':
      table = pd.read_sql_query(f"SELECT * FROM masters join {file_name} using(code_no) where d_type = '{filter}'", conn)
      to_excel(table)
      
    elif filter == 'M' or filter == 'Q':
      table = pd.read_sql_query(f"SELECT * FROM masters join {file_name} using(code_no) where r_type = '{filter}'", conn)
      to_excel(table)
      
    elif filter == 'P' or filter == 'F':
      if file_name == "r9":
         table = pd.read_sql_query(f"SELECT * FROM masters join {file_name} using(code_no) where status = '{filter}'", conn)
         to_excel(table)
         
      else:
         table = pd.read_sql_query(f'''SELECT *
           FROM masters join {file_name} using(code_no) where {month} = '{filter}' ''', conn)
         to_excel(table)
         
    
    return send_file(path, as_attachment=True)


@app.route('/modify', methods=["POST", "GET"])
def modify():
    conn = sqlite3.connect('static/data/data.db')
    cur= conn.cursor()
    cur.execute('SELECT * from masters')
    rows=cur.fetchall()
    if request.method == 'POST':
       info = request.form['action']
       list = info.split()
       if list[0]=="show":
          cur.execute(f"SELECT * from masters where code_no = '{list[1]}'")
          row=cur.fetchone()
          return render_template('masters_modify.html', row=row)
          
       else :
          cur.execute(f"SELECT * from masters where code_no= '{list[1]}'")
          row=cur.fetchone()
          cur.execute(f'''insert into cancelled (code_no, name, gst_no, working_hand, r_type, d_type)
          values({row[1]}, '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}')''')
          cur.execute(f"delete from masters where code_no = '{list[1]}'")
          cur.execute(f"delete from r1 where code_no = '{list[1]}'")
          cur.execute(f"delete from r3b where code_no = '{list[1]}'")
          cur.execute(f"delete from r9 where code_no = '{list[1]}'")
          conn.commit()
          return f"deleted master {list[1]}"
          
    else:
      return render_template('modify.html', rows=rows)
    

@app.route('/masters-modify', methods=["POST", "GET"])
def masters_modify():
        file_no=request.form['File No.']
        name=request.form['Name']
        gst_no=request.form['Gst_No.']
        wh=request.form['Working_hand']
        r_type=request.form['r_type']
        d_type=request.form['d_type']
        old_code=request.form['old_code']
        conn = sqlite3.connect('static/data/data.db')
        cur= conn.cursor()
        # update table masters
        cur.execute(f'''UPDATE masters 
        SET code_no = '{file_no}', name='{name}', gst_no='{gst_no}', 
        working_hand='{wh}', r_type='{r_type}', 
        d_type='{d_type}'  where code_no="{old_code}" ''')
        # update table r1
        cur.execute(f"UPDATE r1 SET code_no ={file_no} where code_no={old_code}")
        # update table r3b
        cur.execute(f"UPDATE r3b SET code_no ={file_no} where code_no={old_code}")
        # update table r9
        cur.execute(f"UPDATE r9 SET code_no ={file_no} where code_no={old_code}")
        conn.commit()
        return redirect("/modify")

@app.route('/search-masters', methods=['POST', 'GET'])
def search_masters():
    search_term = request.form['searchTerm']
    col = request.form['searchBy']
    table = request.form['table'] 
    # Perform database query or any other search logic here
    conn = sqlite3.connect('static/data/data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    try:
         cur.execute(
            f"SELECT code_no, name, gst_no FROM {table} where {col} like '%{search_term}%'"
            )
    except:
          cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    return jsonify(rows)


if __name__ == '__main__':
    app.run(debug=True)
