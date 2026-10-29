


from django.shortcuts import render, redirect


import pandas as pd
import category_encoders as ce
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder


# Create your views here.
from myapp.models import Prediction_table


def add_pred(request):

    return render(request,'prediction.html')

def add_pred_post(request):
    a = request.POST['age']
    g = request.POST['gender']
    e = request.POST['education_level']
    o = request.POST['occupation']
    m = request.POST['marital_status']
    i = request.POST['income']
    c = request.POST['credit_score']

    print(a,g,e,o,m,i,c)


    data = pd.read_csv('myapp/media/loan.csv')

    df = pd.DataFrame(data)

    loan_encoder = LabelEncoder()
    marital_encoder = LabelEncoder()
    gender_encoder = LabelEncoder()

    df['loan_status'] = loan_encoder.fit_transform(df['loan_status'])
    df['marital_status'] = marital_encoder.fit_transform(df['marital_status'])
    df['gender'] = gender_encoder.fit_transform(df['gender'])

    x = df.drop('loan_status', axis=1)
    y = df['loan_status']

    b_encoder = ce.BinaryEncoder(cols=['education_level', 'occupation'])
    x = b_encoder.fit_transform(x)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = XGBClassifier(n_estimators=50, random_state=42)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    encoded_g = gender_encoder.transform([g])[0]
    encoded_m = marital_encoder.transform([m])[0]

    newdata = pd.DataFrame({
            'age':[int(a)],
            'gender':[encoded_g],
            'occupation':[o],
            'education_level':[e],
            'marital_status':[encoded_m],
            'income':[int(i)],
            'credit_score':[int(c)],


     })


    newdata = b_encoder.transform(newdata)
    prediction = model.predict(newdata)

    prediction_value = int(prediction[0])

    request.session['prediction'] = prediction_value

    print(prediction_value)

    p = Prediction_table()

    p.age = a
    p.gender = g
    p.education_level = e
    p.occupation = o
    p.marital_status = m
    p.income = i
    p.credit_score = i

    if (prediction_value == 0):
        p.status = 'Approved'
    else :
        p.status ='Denied'

    p.save()


    return redirect('/myapp/result/')

def result(request):

    prediction = request.session['prediction']

    print(prediction)

    if (prediction == 0):
        result = 'Approved'
    else :
        result = 'Denied'

    return render(request,'result.html',{'data':result})