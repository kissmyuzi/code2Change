from flask import Flask, render_template, request, jsonify
import csv
import random, string
import json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def landing():
    return render_template("landing.html")

@app.route('/addressForm', methods = ['GET', 'POST'])
def submitForm():
    return render_template("addressForm.html")

@app.route('/loginPlanners', methods = ['POST'])
def loginPlanners():
    return render_template("loginPlanners.html")

@app.route('/mainForm', methods = ['POST', 'GET'])
def form():
    if request.method == 'POST':
        refNum = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        result = request.form
        with open("addressDB.txt", "a") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow([refNum, result["Address"], result["City"], result["State"], result["ZIP"]])

    address = result["Address"] + " "+ result["City"] + " " + result["State"] + " " + result["ZIP"]

    return render_template("mainForm.html", refNum=refNum, address=address)

@app.route('/confirm/<string:ref>',methods = ['POST', 'GET'])
def finish(ref):
    if request.method == 'POST':
        refNum = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        result = request.form
        with open("formDB.txt", "a") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow([ref, result["devtype"], result["height"], result["squareMeters"]])


    with open('./templates/ref_json.json') as json_obj:
        data = json.load(json_obj)
    print(data['Fairfield']['Local Center'])
    new_data = data["Fairfield"]['Local Center']
    # return_result = {}
    # return_result['error'] = []
    error = {}
    errorFound = False
    count = 0
    print('Data items: ',new_data.items())
    for key, value in new_data.items():
        count += 1
        if count > 2:
            break
        print(key, value, (value >= int(result[key])))
        # return_result[key] = value

        if (value >= int(result[key])):
            error[key] = "normal"
        else:
            error[key] = "error"
            errorFound = True




    return render_template("confirm.html", ref=ref, result=result, error=error, errorFound=errorFound)


@app.route('/admin')
def admin():
    result = []
    with open('formDB.txt') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            result.append([
                ("ref", row[0]),
                ("devtype", row[1]),
                ("height", row[2]),
                ("squareMeters", row[3]),

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
                    ("height", row[2]),
                    ("squareMeters", row[3])
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
