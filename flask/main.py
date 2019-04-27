from flask import Flask, render_template, request, jsonify
import csv
import random, string

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/submitForm', methods = ['GET', 'POST'])
def submitForm():
    return render_template("submitForm.html")

@app.route('/loginPlanners', methods = ['POST'])
def loginPlanners():
    return render_template("loginPlanners.html")

@app.route('/form', methods = ['POST', 'GET'])
def form():
    if request.method == 'POST':
        refNum = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        result = request.form
        with open("addressDB.txt", "a") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow([refNum, result["Address"], result["City"], result["State"], result["ZIP"]])

    address = result["Address"] + " "+ result["City"] + " " + result["State"] + " " + result["ZIP"]

    return render_template("form.html", refNum=refNum, address=address)

@app.route('/confirm/<string:ref>',methods = ['POST', 'GET'])
def finish(ref):
    if request.method == 'POST':
        refNum = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        result = request.form
        with open("formDB.txt", "a") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow([ref, result["devtype"], result["desc"], result["cost"], result["height"]])
    return render_template("confirm.html", ref=ref, result=result)


@app.route('/admin')
def admin():
    result = []
    with open('formDB.txt') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            result.append([
                ("ref", row[0]),
                ("devtype", row[1]),
                ("desc", row[2]),
                ("cost", row[3]),
                ("height", row[4]),
            ])

    return render_template("admin.html", data=result)

@app.route('/view/<string:ref>')
def view(ref):
    result = []
    address = ""
    with open('addressDB.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if (row[0] == ref):
                address = row[1] + " "+ row[2] + " " + row[3] + " " + row[4]

    with open('formDB.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if (row[0] == ref):
                result = [
                    ("ref", row[0]),
                    ("devtype", row[1]),
                    ("desc", row[2]),
                    ("cost", row[3]),
                    ("height", row[4]),
                ]
                return render_template("view.html", address=address, data=result)

@app.route("/search", methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
        print(request.form)
        return view(request.form["refNum"])
    return render_template("search.html")

if __name__ == '__main__':
   app.run(debug = True)
