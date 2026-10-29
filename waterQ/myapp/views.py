from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group,User
from django.shortcuts import render, redirect


# Create your views here.
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import shap

from myapp.models import User_table, Prediction_table, Complaints, Feedback_table


def login_get(request):
    return render(request,'login.html')

def login_post(request):
    username = request.POST['username']
    password = request.POST['pwrd']
    user = authenticate(request,username=username,password = password)
    if user is not None:
        login(request,user)
        if user.groups.filter(name='admin').exists():
            return redirect('/myapp/admin_home/')
        elif user.groups.filter(name='user').exists():
            return redirect('/myapp/user_home/')
        else:
            messages.error(request,'User profile not found:')
            return redirect('/myapp/login_get/')
    else:
        messages.error(request,'invalid username or password')
        return redirect('/myapp/login_get/')



# -----------------------------------admin---------------------------------------------


def admin_home(request):
    return render(request,'admin/home.html')

def admin_view_user(request):
    u = User_table.objects.all()
    return render(request,'admin/view_user.html',{'data':u})

def admin_view_predictions(request):
    p = Prediction_table.objects.all()
    return render(request,'admin/view_predictions.html',{'data':p})

def admin_view_complaints(request):
    c = Complaints.objects.all()
    return render(request,'admin/view_complaints.html',{'data':c})

def reply(request,id):
    c = Complaints.objects.get(id= id)
    request.session['id'] = c.id
    return render(request,'admin/reply.html')

def reply_post(request):
    cid = request.session['id']
    r = request.POST['reply']

    c = Complaints.objects.get(id = cid)

    c.reply = r
    c.save()
    return redirect('/myapp/admin_view_complaints/')

def admin_view_feedback(request):
    f = Feedback_table.objects.all()
    return render(request,'admin/view_feedback.html',{'data':f})










# -----------------------------------user-------------------------------


def user_register(request):
    return render(request,'user/register.html')


def user_reqister_post(request):
    n = request.POST['name']
    uname = request.POST['uname']
    pwrd = request.POST['pwrd']
    e = request.POST['email']
    p = request.POST['phone']
    a = request.POST['age']
    place = request.POST['place']

    if User.objects.filter(username=uname).exists():
        messages.warning(request,'username is already registered')
        return redirect('/myapp/login_get/')


    u = User.objects.create(username=uname ,password = make_password(pwrd))
    group = Group.objects.get(name='user')
    u.groups.add(group)
    u.save()

    user = User_table()

    user.name = n
    user.email = e
    user.phone = p
    user.age = a
    user.place = place
    user.LOGIN= u
    user.save()

    return redirect('/myapp/login_get/')

def user_home(request):

    return render(request,'user/home.html')

def view_user_profile(request):
    u = User_table.objects.get(LOGIN = request.user)
    return render(request,'user/view_profile.html',{'data':u})

def edit_user_profile(request):
    u = User_table.objects.get(LOGIN = request.user)
    return render(request,'user/edit_profile.html',{'data':u})

def edit_user_profile_post(request):
    n = request.POST['name']
    e = request.POST['email']
    p = request.POST['phone']
    a = request.POST['age']
    place = request.POST['age']


    u = User_table.objects.get(LOGIN = request.user)

    u.name = n
    u.email = e
    u.phone = p
    u.age = a
    u.place = place
    u.save()

    return redirect('/myapp/view_user_profile/')


def check_quality(request):
    return render(request,'user/check_quality.html')

def check_quality_post(request):

    ph = float(request.POST['ph'])
    tds = float(request.POST['tds'])
    turbidity = float(request.POST['turbidity'])

    uid = User_table.objects.get(LOGIN=request.user)

    data = pd.read_csv(
        r'C:\Users\abin1\PycharmProjects\waterQ\templates\media\water_quality_200_records.csv'
    )

    df = pd.DataFrame(data)

    encoder = LabelEncoder()
    df['Water_Quality'] = encoder.fit_transform(df['Water_Quality'])

    X = df.drop("Water_Quality", axis=1)
    y = df["Water_Quality"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)

    newdata = pd.DataFrame({
        'pH': [ph],
        'TDS': [tds],
        'Turbidity': [turbidity]
    })

    prediction = model.predict(newdata)
    prediction_value = int(prediction[0])

    # Convert the encoded prediction back to the original label
    predicted_label = str(
        encoder.inverse_transform([prediction_value])[0]
    )

    # Calculate SHAP values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(newdata)

    # Explain the predicted class
    class_index = list(model.classes_).index(prediction_value)
    feature_values = shap_values[0, :, class_index].values

    # Store the feature contributions in a dictionary
    shap_data = {
        feature: round(float(value), 4)
        for feature, value in zip(X.columns, feature_values)
    }

    # Convert the dictionary into a display-friendly string
    shap_string = ", ".join(
        f"{feature}: {value}"
        for feature, value in shap_data.items()
    )

    # Save the prediction in the database
    p = Prediction_table()
    p.User = uid
    p.ph = ph
    p.tds = tds
    p.turbidity = turbidity
    p.water_quality = predicted_label
    p.explanation = shap_string
    p.save()

    # Store only JSON-serializable values in the session
    request.session['water_quality'] = predicted_label
    request.session['prediction_value'] = prediction_value
    request.session['explanation'] = shap_data


    return redirect('/myapp/result/')

def result(request):
    # d=Prediction_table.objects.all()
    w = request.session['water_quality']
    e = request.session['explanation']

    return render(request,'user/result.html',{'water_quality':w,'explanation':e})




# def check_quality_post(request):
#     import pandas as pd
#     import shap
#
#     from sklearn.model_selection import train_test_split
#     from sklearn.preprocessing import LabelEncoder
#     from sklearn.ensemble import RandomForestClassifier
#     from django.shortcuts import redirect
#
#     ph = float(request.POST['ph'])
#     tds = float(request.POST['tds'])
#     turbidity = float(request.POST['turbidity'])
#
#     uid = User_table.objects.get(LOGIN=request.user)
#
#     data = pd.read_csv(
#         r'C:\Users\abin1\PycharmProjects\waterQ\templates\media\water_quality_200_records.csv'
#     )
#
#     df = pd.DataFrame(data)
#
#     encoder = LabelEncoder()
#     df['Water_Quality'] = encoder.fit_transform(df['Water_Quality'])
#
#     X = df.drop("Water_Quality", axis=1)
#     y = df["Water_Quality"]
#
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=0.2, random_state=42
#     )
#
#     model = RandomForestClassifier(
#         n_estimators=100,
#         random_state=42
#     )
#     model.fit(X_train, y_train)
#
#     newdata = pd.DataFrame({
#         'pH': [ph],
#         'TDS': [tds],
#         'Turbidity': [turbidity]
#     })
#
#     prediction = model.predict(newdata)
#     prediction_value = int(prediction[0])
#
#     # Convert the encoded prediction back to the original label
#     predicted_label = str(
#         encoder.inverse_transform([prediction_value])[0]
#     )
#
#     # Calculate SHAP values
#     explainer = shap.TreeExplainer(model)
#     shap_values = explainer(newdata)
#
#     # Explain the predicted class
#     class_index = list(model.classes_).index(prediction_value)
#     feature_values = shap_values[0, :, class_index].values
#
#     # Store the feature contributions in a dictionary
#     shap_data = {
#         feature: round(float(value), 4)
#         for feature, value in zip(X.columns, feature_values)
#     }
#
#     # Convert the dictionary into a display-friendly string
#     shap_string = ", ".join(
#         f"{feature}: {value}"
#         for feature, value in shap_data.items()
#     )
#
#     # Save the prediction in the database
#     p = Prediction_table()
#     p.User = uid
#     p.ph = ph
#     p.tds = tds
#     p.turbidity = turbidity
#     p.water_quality = prediction_value
#     p.explanation = shap_string
#     p.save()
#
#     # Store only JSON-serializable values in the session
#     request.session['water_quality'] = predicted_label
#     request.session['prediction_value'] = prediction_value
#     request.session['explanation'] = shap_data

#     return redirect('/myapp/result/')


def user_view_prediction(request):
    uid = User_table.objects.get(LOGIN = request.user)
    p = Prediction_table.objects.filter(User = uid)
    return render(request,'user/predictions.html',{'data':p})

def user_add_complaints(request):
    return render(request,'user/add_complaint.html')

def user_add_complaints_post(request):
    uid = User_table.objects.get(LOGIN = request.user)
    c = request.POST['complaint']

    com = Complaints()

    com.User = uid
    com.complaint = c
    com.save()

    return redirect('/myapp/user_view_complaint/')

def user_view_complaint(request):
    c = Complaints.objects.all()
    return render(request,'user/view_complaint.html',{'data':c})



def user_add_feedback(request):
    return render(request,'user/add_feedback.html')

def user_add_feedback_post(request):
    uid = User_table.objects.get(LOGIN = request.user)
    f = request.POST['feedback']

    feed = Feedback_table()

    feed.User = uid
    feed.feedback = f
    feed.save()

    return redirect('/myapp/user_view_feedback/')

def user_view_feedback(request):
    uid = User_table.objects.get(LOGIN = request.user)
    f = Feedback_table.objects.filter(User = uid)
    return render(request,'user/view_feedback.html',{'data':f})