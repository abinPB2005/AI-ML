import shap
import pandas as pd
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from myapp.models import Prediction_table



def login_get(request):
    return render(request,'login.html')

def login_post(request):
    username = request.POST['uname']
    password = request.POST['pwrd']

    user = authenticate(request,username = username,password = password)
    if user is not None:
        login(request,user)
        if user.groups.filter(name='admin').exists():
            return redirect('/myapp/home/')
        else :
            messages.error(request,'User profile not found :')
            return redirect('/myapp/login_get/')

    else :
        messages.error(request,'invalid username or password')
        return redirect('/myapp/login_get/')


def home(request):
    return render(request,'home.html')

def check_diabet(request):
    return render(request,'check_diabet.html')

def check_diabet_post(request):
    p = int(request.POST['pregnancies'])
    g = int(request.POST['glucose'])
    bp = int(request.POST['bloodpressure'])
    st = int(request.POST['skinthickness'])
    i = int(request.POST['insulin'])
    bmi = float(request.POST['bmi'])
    dpf = float(request.POST['diabetespedigreefunction'])
    a = int(request.POST['age'])

    data = pd.read_csv(r'C:\Users\abin1\PycharmProjects\diabetPro\templates\diabetes.csv')
    df = pd.DataFrame(data)

    x = df.drop("Outcome", axis=1)
    y = df["Outcome"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    newdata = pd.DataFrame({
        "Pregnancies": [p],
        "Glucose": [g],
        "BloodPressure": [bp],
        "SkinThickness": [st],
        "Insulin": [i],
        "BMI": [bmi],
        'DiabetesPedigreeFunction': [dpf],
        'Age': [a]
    })

    prediction = model.predict(newdata)
    prediction_value = int(prediction[0])

    explainer = shap.Explainer(model)
    shap_values = explainer(newdata)
    class_index = list(model.classes_).index(prediction_value)
    feature_values = shap_values[0, :, class_index].values

    # Store the feature contributions in a dictionary
    shap_data = {
        feature: round(float(value), 4)
        for feature, value in zip(x.columns, feature_values)
    }

    # Convert the dictionary into a display-friendly string
    shap_string = ", ".join(
        f"{feature}: {value}"
        for feature, value in shap_data.items()
    )

    pre = Prediction_table()

    print(shap_string)
    print(prediction_value)

    pre.pregnancies = p
    pre.glucose = g
    pre.bloodPressure = bp
    pre.skinThickness = st
    pre.insulin = i
    pre.bMI = bmi
    pre.diabetesPedigreeFunction = dpf
    pre.age = a
    pre.outcome = prediction_value
    pre.explanation = shap_string
    pre.save()

    request.session['outcome'] = prediction_value
    request.session['explanation'] = shap_string

    return redirect('/myapp/result/')


def result(request):

    o =  request.session['outcome']
    ex = request.session['explanation']

    if o == 1 :
        outcome = 'diabetes'
    else :
        outcome = 'non-diabetes'
    return render(request,'result.html',{'outcome':outcome,'explanation':ex})


def all_prediction(request):
    p = Prediction_table.objects.all()
    return render(request,'all_predictions.html',{'data':p})

