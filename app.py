from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

#Set up DB
DATABASE = 'toDoList.db'

#Use database without values
def sql(cmd):
  conn = sqlite3.connect(DATABASE)
  cur = conn.cursor()
  query = cur.execute(cmd).fetchall()
  conn.commit()
  conn.close()
  return query

#Use database with values
def sqlVal(cmd, vals=None):
  conn = sqlite3.connect(DATABASE)
  cur = conn.cursor()
  query = cur.execute(cmd, vals).fetchall()
  conn.commit()
  conn.close()
  return query

@app.route('/')
def start_page():
  query = sql('SELECT * FROM toDoList')
  return render_template("index.html", query = query)

#Render Page to add Post
@app.route('/addToDo')
def add_blog_post():
  return render_template("addToDo.html")

#Render/Re-render post confirmation or page to add new task
@app.route('/addToDo', methods=["POST"])
def create_post():
  #Input info
  name = str(request.form.get("Name"))
  description = str(request.form.get("Description"))
  motivation = str(request.form.get("Motivation"))

  

  nameLen = len(name)
  descriptionLen = len(description)
  motivationLen = len(motivation)
  print(motivation)
  print(motivationLen)

  emptyError = "Please fill in the Name and Description fields. The motivation field is optional."
  nameError = "Name must be between 1 and 100 characters"
  otherError = "Entry must be between 1 and 1000 characters"

  if name == "" or description == "":
    return render_template("addToDo.html", emptyError = emptyError)
  elif nameLen <= 0 or nameLen > 100:
    return render_template("addToDo.html", nameError = nameError)
  elif descriptionLen > 0 and descriptionLen < 1000 and motivationLen >= 0 and motivationLen < 1000:
    #Insert into DB
    sqlVal('INSERT INTO toDoList (name, description, motivation) VALUES (?, ?, ?)', (name, description, motivation))
    return render_template("toDoAdded.html", name = name, description = description, motivation = motivation)
  else:
    return render_template("addToDo.html", otherError = otherError)
    
@app.route('/removedTask')
def remove():
  name = request.args.get('name')
  error = "Could not find a task with that name"
  if name != None:
    query = sqlVal('DELETE FROM toDoList WHERE name = (?)', (name,))
    return render_template('removedTask.html', name = name)
  return render_template('removedTask.html', error = error)



app.run(host='0.0.0.0', port=5000)