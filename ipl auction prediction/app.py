import numpy as np
import pickle
import catboost
from catboost import CatBoostRegressor

from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__, template_folder='template')
app.secret_key = 'key'
model = pickle.load(open('ipl.pkl', 'rb'))

@app.route('/')
@app.route('/')
def home():
    session['nameVal'] = {}
    session['curVal'] = "${:,.2f}".format(12030111.84)
    session['playerCount'] = 0
    return render_template("index.html", nameVal=session['nameVal'], curVal=session['curVal'], playerCount=session['playerCount'])

@app.route('/predict', methods=['POST'])
def predict():
    int_features = list(request.form.values())
    name = int_features[0]
    int_features = int_features[1:]
    int_features = [float(x) for x in int_features]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0], 2)
        
    session['name'] = name
    session['output'] = output 
    return render_template('index.html', name='{}'.format(name), prediction_value='Prediction value : ${}'.format(output), curVal=session['curVal'], playerCount=session['playerCount'])

@app.route('/discard', methods=['GET', 'POST'])
def discard():
    return render_template('index.html', name='', prediction_value='Prediction value : $', playerCount=session['playerCount'], curVal=session['curVal'])

@app.route('/addPlayer', methods=['GET', 'POST'])
def addPlayer():
    output = session.get('output', 0)
    name = session.get('name')
    
    nameVal = session.get('nameVal', {})

    if session['playerCount'] >= 25:
        flag = "Player count limit reached. Cannot add more players."
        return render_template('index.html', name='{}'.format(name), prediction_value='Prediction value : ${}'.format(output), nameVal=session['nameVal'], playerCount=session['playerCount'], flag=flag, curVal=session['curVal'])
    
    curVal_str = session.get('curVal', '0').replace('$', '').replace(',', '')
    try:
        curVal = float(curVal_str)
    except ValueError:
        curVal = 0.0

    if curVal - output < 0:
        flag = "Insufficient budget to add this player."
        return render_template('index.html', name='{}'.format(name), prediction_value='Prediction value : ${}'.format(output), nameVal=session['nameVal'], playerCount=session['playerCount'], flag=flag, curVal=session['curVal'])

    if name not in nameVal:
        session['playerCount'] = session.get('playerCount', 0) + 1
        curVal -= output
        session['curVal'] = "${:,.2f}".format(curVal)
    else:
        flag = f"{name} already exists!"
        return render_template('index.html', name='{}'.format(name), prediction_value='Prediction value : ${}'.format(output), nameVal=session['nameVal'], playerCount=session['playerCount'], flag=flag, curVal=session['curVal'])

    nameVal[name] = output
    session['nameVal'] = nameVal

    return render_template('index.html', name='{}'.format(name), prediction_value='Prediction value : ${}'.format(output), nameVal=session['nameVal'], playerCount=session['playerCount'], flag='', curVal=session['curVal'])

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    session['nameVal'] = {}
    session['curVal'] = "${:,.2f}".format(12030111.84)
    session['playerCount'] = 0
    return redirect(url_for('home'))

@app.route('/view_team')
def view_team():
    nameVal = session.get('nameVal', {})
    curVal = session.get('curVal', 0)
    return render_template('view_team.html', nameVal=nameVal, curVal=curVal)

@app.route('/home_view')
def home_view():
    nameVal = session.get('nameVal', {})
    curVal = session.get('curVal', 0)
    return render_template('index.html', nameVal=nameVal, curVal=curVal, playerCount=session['playerCount'])

if __name__ == "__main__":
    app.run(debug=True)

