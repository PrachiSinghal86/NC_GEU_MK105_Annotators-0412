from flask import Flask,render_template,request,redirect,session,flash,url_for
import mysql.connector
from flask_mysqldb import MySQL
import os
import MySQLdb.cursors
import re
import pandas as pd
from rating import addjob
from keras.models import  model_from_json
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from datetime import datetime

#Analysis
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from palettable.colorbrewer.qualitative import Pastel1_7

#Rnn model
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence

#Salary analysis
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import warnings
warnings.simplefilter(action='ignore')

app = Flask(__name__)
app.secret_key=os.urandom(24)

#config db
#db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MySQL@2000'
app.config['MYSQL_DB'] = 'registration_sih'
conn = MySQL(app)

@app.route('/')
def First_home():
    return render_template('First_home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/home')
def home():
        # Check if user is loggedin
        if 'loggedin' in session:
            # User is loggedin show them the home page
            return render_template('home.html', email=session['email'])
        # User is not loggedin redirect to login page
        return redirect('/login')

@app.route('/about')
def about_home():
    return render_template('about.html')

############## PROFILE BUILDING ###########

@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        '''cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_register WHERE id = %s', (session['ID'],))
        account = cursor.fetchone()'''
        ID = session['ID']
        cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * from user_register where ID=%s", (ID,))
        pro1 = cursor.fetchone()

        # Show the profile page with account info
        return render_template('profile.html', pro1=pro1)
    # User is not loggedin redirect to login page
    return redirect('/login')


@app.route('/profile_validation', methods=['GET', 'POST'])
def profile_validation():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' :
        # Create variables for easy access
        contact_no = request.form.get('contact_no')
        country = request.form.get('country')
        industry = request.form.get('industry')
        stream = request.form.get('stream')
        work_exp = request.form.get('work_exp')
        degree = request.form.get('degree')
        about = request.form.get('about')

        ID=session['ID']

        cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * from user_register where ID=%s", (ID,))
        pro1 = cursor.fetchone()

        cursor.execute('UPDATE user_register set contact_no= %s , country =%s, industry = %s, stream =%s, work_exp = %s, degree = %s, about=%s  WHERE ID= %s',( contact_no, country, industry, stream, work_exp, degree, about , ID,));
        conn.connection.commit()
        flash('You have successfully updated your profile!')
        return render_template('profile.html',pro1=pro1)
    else:
        ID = session['ID']

        cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * from user_register where ID=%s", (ID,))
        pro1 = cursor.fetchone()
        flash('Enter valid response')
        return render_template('profile.html',pro1=pro1)

@app.route('/skill_validation', methods=['POST','GET'])
def skill_validation():
        ID = session['ID']
        skill = request.form.get('skill')
        rate = request.form.get('rate')

        cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM skill_set WHERE ID = %s and skill = %s', (ID,skill,))
        account1 = cursor.fetchone()

        if account1:
            flash("Skill already exists")
            return redirect(url_for('profile'))
        else:
            cursor.execute("""INSERT INTO `skill_set` ( `ID`,`skill`,`rate`) VALUES
                            ('{}','{}','{}')""".format(ID, skill, rate))
            conn.connection.commit()
            flash("Skill added")
            return redirect(url_for('profile'))
        return redirect('/profile')


@app.route('/display_skillset')
def display_skillset():
        ID = session['ID']
        cur = conn.connection.cursor()
        resultValue= cur.execute("SELECT * from skill_set where ID=%s",(ID,))

        skillDetails= cur.fetchall()
        resultValue1 = cur.execute("SELECT * from interpersonal_skill_set where ID=%s", (ID,))

        skillDetails1 = cur.fetchall()
        if resultValue > 0 or resultValue1 > 0:
            return render_template('skillset.html', skillDetails=skillDetails, skillDetails1=skillDetails1 )
        else:
            flash("Add skills")
            return redirect(url_for('profile'))


@app.route('/interpersonal_skill_validation', methods=['GET','POST'])
def interpersonal_skill_validation():
            ID = session['ID']
            skill = request.form.get('skill')
            rate = request.form.get('rate')

            cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM interpersonal_skill_set WHERE ID = %s and skill = %s', (ID,skill,))
            account1 = cursor.fetchone()

            if account1:
                flash("Skill already exists")
                return redirect(url_for('profile'))
            else:
                cursor.execute("""INSERT INTO `interpersonal_skill_set` ( `ID`,`skill`) VALUES
                                ('{}','{}')""".format(ID, skill))
                conn.connection.commit()
                flash("Skill added")
                return redirect(url_for('profile'))
            return redirect('/profile')


@app.route('/update_tech_validation',methods=['GET','POST'])
def update_tech_validation():
        ID = session['ID']
        u_skill= request.form.get('u_skill')
        u_rate = request.form.get('u_rate')

        cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE skill_set set rate=%s WHERE ID = %s and skill = %s', (u_rate,ID, u_skill,))
        conn.connection.commit()
        flash("Skill Updated")
        return redirect(url_for('display_skillset'))

@app.route('/update_inter_validation',methods=['GET','POST'])
def update_inter_validation():
        ID = session['ID']
        u1_skill= request.form.get('u1_skill')
        u1_rate = request.form.get('u1_rate')

        cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(' DELETE from interpersonal_skill_set WHERE ID = %s and skill = %s', (ID, u1_skill,));
        conn.connection.commit()
        flash("Skill Deleted")
        return redirect(url_for('display_skillset'))

                            ################### END PROFILE BUILDING ##########################

                            ############################## User end ###########################
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/login_validation', methods=['GET', 'POST'])
def login_validation():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_register WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['ID'] = account['ID']
            session['email'] = account['email']
            flash('Logged in Successfully!')
            # Redirect to home page
            return redirect('/home')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password!')
            return render_template('login.html', msg=msg)
    # Show the login form with message (if any)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_register WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user_register (username, password, email) VALUES (%s, %s, %s)', (username, password, email,))
            conn.connection.commit()
            flash('You have successfully registered!')
            return render_template('login.html')

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')

                ######################## END USER END ########################

    ############Recruiter END#############
@app.route('/rec_profile')
def rec_profile():
    return render_template('rec_profile.html')

@app.route('/rec_login')
def rec_login():
    return render_template('rec_login.html')

@app.route('/rec_register')
def rec_register():
    return render_template('rec_register.html')

@app.route('/rec_add_job')
def rec_add_job():
    return render_template('add_job.html')

@app.route('/rec_add_user', methods=['GET', 'POST'])
def rec_add_user():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            # Check if account exists using MySQL
            cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM rec_register WHERE email = %s', (email,))
            account = cursor.fetchone()
            # If account exists show error and validation checks
            if account:
                flash('Account already exists!')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!')
            elif not re.match(r'[A-Za-z0-9]+', username):
                flash('Username must contain only characters and numbers!')
            elif not username or not password or not email:
                flash('Please fill out the form!')
            else:
                cursor.execute('INSERT into rec_register (username,password,email) values (%s,%s,%s) ',
                               (username, password, email))
                conn.connection.commit()
                flash('You have successfully registered!')
                return redirect(url_for('rec_login'))

    elif request.method == 'POST':
        flash('Please fill out the form!')
        return redirect(url_for('rec_register'))
    return redirect(url_for('rec_register'))

@app.route('/rec_login_validation', methods=['GET', 'POST'])
def rec_login_validation():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            # Create variables for easy access
            #email = request.form['email']
            #password = request.form['password']
            email = request.form.get('email')
            password = request.form.get('password')
            # Check if account exists using MySQL
            cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM rec_register WHERE email = %s AND password = %s', (email, password,))
            # Fetch one record and return result
            account = cursor.fetchone()
            # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['ID'] = account['ID']
                session['email'] = account['email']

                ID = session['ID']
                cursor.execute("SELECT * from rec_register where ID=%s", (ID,))
                pro = cursor.fetchone()
                return render_template('rec_profile.html', pro=pro)

            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password!')
                return redirect(url_for('rec_login'))

    # Recruiter profile
@app.route('/rec_profile_validation', methods=['GET', 'POST'])
def rec_profile_validation():
        # Create variables for easy access
    if request.method == 'POST':
            companyname = request.form.get('companyname')
            sector = request.form.get('sector')
            website = request.form.get('website')

            rec_number = request.form.get('rec_number')
            rec_city = request.form.get('rec_city')
            rec_country = request.form.get('rec_country')
            rec_address = request.form.get('rec_address')
            ID = session['ID']
            cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * from rec_register where ID= %s", (ID,))
            pro = cursor.fetchone()

            cursor.execute(
                'UPDATE rec_register set companyname= %s , sector =%s, website = %s, rec_city =%s, rec_country = %s, rec_address = %s  WHERE ID= %s',
                (companyname, sector, website, rec_city, rec_country, rec_address, ID,));
            conn.connection.commit()
            flash('You have successfully updated your profile!')
            return render_template('rec_profile.html', pro=pro)

@app.route('/add_job', methods=['POST'])
def save_content():
        # This is to make sure the HTTP method is POST and not any other
        if request.method == 'POST':
            Title = request.form.get('Title')
            Location = request.form.get('Location')
            Company = request.form.get('Company')
            Salary = request.form.get('Salary')
            Description = request.form.get('Description')
            status = addjob(Title, Location, Company, Salary, Description)
            flash(status)
            return render_template('add_job.html')
            # return status

            ##################### END RECRUITER END #######################

                        #######################RNN model #####################################

@app.route('/filename')
def filename():
    return render_template('filename.html')

@app.route('/predict',methods = ['POST','GET'])
def predict():
    ID = session['ID']
    cur = conn.connection.cursor()

    r1 = cur.execute("SELECT about from user_register WHERE ID = %s ", (ID,))
    about1 = cur.fetchall()
    about1 = list(about1)
    about1 = [item for t in about1 for item in t]
    about2 = []
    for i in about1:
        about2.append(i)

    r2 = cur.execute('SELECT * FROM skill_set WHERE ID = %s ', (ID,))
    s1 = cur.fetchall()

    r3 = cur.execute('SELECT skill FROM interpersonal_skill_set WHERE ID = %s ', (ID,))
    s2 = cur.fetchall()

    r4 = cur.execute("SELECT work_exp from user_register WHERE ID = %s ", (ID,))
    w_exp = cur.fetchall()
    w_exp = list(w_exp)
    w_exp1 = [item for t in w_exp for item in t]
    w_exp2=[]
    for i in w_exp1:
        w_exp2.append(i)
    r5 = cur.execute("SELECT degree from user_register WHERE ID = %s ", (ID,))
    degree1 = cur.fetchall()
    degree1 = list(degree1)
    degree1 = [item for t in degree1 for item in t]
    degree2 = []
    for i in degree1:
        degree2.append(i)
    summary = ""
    summary = summary + str(about2[0]) + "." + " My highest educational qualification(degree) is " + str(degree2[0]) + ". years."+ "His technical skills are "
    for i in s1:
        summary = summary + i[1] + ":"
        if i[2] == 1:
            var = "Beginner"
        elif i[2] == 2:
            var = "Intermediate"
        else:
            var = "Expert"
        summary = summary + var + ","
    summary = summary + "His interpersonal skills are "
    for j in s2:
        summary = summary + j[0] + ","
    summary = summary + "He has a work experience of " + str(w_exp2[0]) + " years."

    json_file = open('model1.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model1.h5")
    # print("Loaded model from disk")

    data = pd.read_csv("rnn_dataset.csv")

    MAX_NB_WORDS = 5000
    MAX_SEQUENCE_LENGTH = 200
    EMBEDDING_DIM = 100
    tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
    tokenizer.fit_on_texts(data['Description'].values)
    word_index = tokenizer.word_index
    labels = ['App Developer',
              'Cloud and DevOps Engineer',
              'Data Scientist and Analyst',
              'Full Stack Developer',
              'Machine Learning Engineer',
              'Software Developer',
              'Web Developer']

    def predictions(pred):
        predictions_list = []
        pred_reshape = np.reshape(pred, (7, 1))
        list_pred = pred_reshape.tolist()
        [list_pred[i].append(i + 1) for i in range(0, len(list_pred))]
        list_pred.sort(key=lambda x: x[0], reverse=True)
        for i in range(0, len(list_pred)):
            predictions_list.append(labels[list_pred[i][1] - 1] + " - " + str("{:.2f}".format(list_pred[i][0] * 100) + " %"))
        return predictions_list

    new_role = []
    new_role.append(summary)
    #new_role = ["working vision sensor fusion system focusing automotive ada iot machine condition monitoring required skill knowledge different deep learning practice cnn rnn ltsm reinforcement learning ssd inception googlenet yolo etc machine learning general machine learning programming expert computer vision image processing opencv opencv cuda caffe tensorflow model training software fluent python c c linux platform object detection classification dnn model using nvidia ai board intel nc low power embedded device inference added contribution research community publishing paper participation github project related deep learning preferred advanced degree phd post graduation machine learning computer science embedded plus qualification b tech tech electronics electrical computer engineering 3 year 3 12 year bangalore"]### INPUT data - request.form.values()
    seq = tokenizer.texts_to_sequences(new_role)
    padded = sequence.pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH)
    pred = loaded_model.predict(padded)

    final_predictions = predictions(pred)
    output = pd.Series(final_predictions).head(3).tolist()
    predictedValue =[]
    predictedtitle = []
    for j in output:
        predictedtitle.append(j.split('-')[0])
        predictedValue.append(j.split('-')[1])

    #Top:
    MLE_T= ['Machine Learning', 'Python', 'AI', 'Tensorflow', 'Deep Learning', 'R', 'CNN', 'Computer Vision']
    FSD_T = ['HTML', 'CSS', 'Javascript', 'Rest API', 'SQL', 'Nodejs', 'Mongodb', 'Angularjs']
    SD_T = ['Java', '.net', 'OOPSs', 'SQL', 'Python', 'vb.net', 'mvc']
    DSA_T = ['Python', 'R', 'SQL', 'Spark', 'Tableau', 'Hadoop', 'Statistics']
    WD_T = ['HTML', 'CSS', 'Javascript', 'PHP', 'Wordpress', 'Bootstrap', 'git', 'Ajax']
    AD_T = ['Java', 'Swift', 'Android SDK', 'Objective C', 'git', 'ios', 'Cocoa', 'Json']
    CDE_T = ['AWS', 'Linux', 'Azure', 'Kubernetes', 'Jenkins', 'Devops', 'GCP', 'Docker']

    suggestion=[]
    ID = session['ID']
    cur = conn.connection.cursor()
    cur.execute("SELECT skill from skill_set where ID=%s", (ID,))
    req = cur.fetchall()
    req = list(req)
    req1 = [item for t in req for item in t]
    req2=[]
    for i in req1:
        req2.append(i.lower())
    if predictedtitle[0] == "Web Developer ":
        top = WD_T
        a = "https://www.naukri.com/web-developer-jobs"
        for j in WD_T:
            if j.lower() not in req2:
                suggestion.append(j)

    elif predictedtitle[0] == "Machine Learning Engineer ":
        top = MLE_T
        a = "https://www.indeed.co.in/Machine-Learning-jobs"
        for j in MLE_T:
            if j.lower() not in req2:
                suggestion.append(j)

    elif predictedtitle[0] == "Cloud and DevOps Engineer ":
        top = CDE_T
        a = "https://www.naukri.com/cloud-devops-jobs"
        for j in CDE_T:
            if j.lower() not in req2:
                suggestion.append(j)

    elif predictedtitle[0] == "App Developer ":
        top = AD_T
        a = "https://www.naukri.com/application-developer-jobs"
        for j in AD_T:
            if j.lower() not in req2:
                suggestion.append(j)

    elif predictedtitle[0] == "Data Scientist and Analyst ":
        top = DSA_T
        a = "https://www.naukri.com/machine-learning-jobs-in-india"
        for j in DSA_T:
            if j.lower() not in req2:
                suggestion.append(j)

    elif predictedtitle[0] == "Software Developer ":
        top = SD_T
        a = "https://www.indeed.co.in/Software-Developer-jobs"
        for j in SD_T:
            if j.lower() not in req2:
                suggestion.append(j)

    elif predictedtitle[0] == "Full Stack Developer ":
        top = FSD_T
        a = "https://www.glassdoor.co.in/Job/india-full-stack-web-developer-jobs-SRCH_IL.0,5_IN115_KO6,30.htm"
        for j in FSD_T:
            if j.lower() not in req2:
                suggestion.append(j)


    #salary prediction##
    r5 = cur.execute('SELECT country FROM user_register WHERE ID = %s ', (ID,))
    locate1 = cur.fetchall()

    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
                 "you'll",
                 "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
                 "she's",
                 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs',
                 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',
                 'am',
                 'is',
                 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                 'did',
                 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
                 'at',
                 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
                 'after',
                 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
                 'again',
                 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
                 'both',
                 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
                 'same',
                 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
                 "should've",
                 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
                 'didn',
                 "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn',
                 "isn't",
                 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
                 'shouldn',
                 "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",
                 'role',
                 'risk', 'specialist', 'company', 'program', 'multiple', 'process', 'machine', 'data']

    locate1 = list(locate1)
    locate1 = [item for t1 in locate1 for item in t1]
    locate2 = []
    for i in locate1:
        locate2.append(i)

    location1 = str(locate2[0])
    title1 = predictedtitle[0]
    location = location1
    title = title1
    data = [[location, title]]
    df1 = pd.DataFrame(data, columns=['Location', 'Title'])

    svm_from_joblib = joblib.load('model_salary.pkl')
    # defining custom stop words of Tfidf
    custom_stop_words = ['role', 'risk', 'specialist', 'company', 'program', 'multiple', 'process', 'machine',
                         'data']
    # stopwords=stopwords.words('english')
    stopwords.extend(custom_stop_words)

    # define a funciton to generate tfidf vector from text data
    def create_tfidf_vec(data):
        tfidf = TfidfVectorizer(stop_words=stopwords, max_df=1000, min_df=1, sublinear_tf=True,
                                ngram_range=(1, 2))
        tfidf.fit(data)
        X_vec = pd.DataFrame(tfidf.transform(data).todense(), columns=tfidf.get_feature_names())
        return X_vec

    col_names = ['analyst', 'app', 'app developer', 'cloud', 'cloud devops', 'devops', 'devops engineer',
                 'engineer',
                 'full', 'full stack', 'learning', 'learning engineer', 'research', 'research analyst',
                 'scientist',
                 'scientist analyst',
                 'software', 'software developer', 'stack', 'stack developer', 'web', 'web developer',
                 'Ahmedabad',
                 'Bengaluru',
                 'Chennai', 'Coimbatore', 'Delhi', 'Gurgaon', 'Hyderabad', 'India', 'Indore', 'Jaipur', 'Kochi',
                 'Kolkata',
                 'Mohali', 'Mumbai',
                 'New Delhi', 'Noida', 'Others', 'Pune', 'Surat']

    def single_prediction(var, index):
        var1 = var['Title']
        var_vec = create_tfidf_vec(var1)
        var_vector = np.zeros((1, 41))
        df = pd.DataFrame(var_vector, columns=col_names)
        for i in var_vec.columns:
            if i in df.columns:
                df[i] = var_vec[i]
            if var['Location'][index] in df.columns:
                df[var['Location']] = 1
            else:
                df['Others'] = 1
        prediction = svm_from_joblib.predict(df)
        if prediction == 'High':
            return "4,50,000 - 9,00,000"
        elif prediction == 'Medium':
            return "2,50,000 - 4,50,000"
        else:
            return "Below 2,50,000"

    sal_prediction1 = ""
    sal_prediction1 = single_prediction(df1, 0)
    ##salary prediction##

    #display result
    resultValue = cur.execute("SELECT * from skill_set where ID=%s", (ID,))
    if resultValue > 0 :
        return render_template('filename.html',a=a, sal_prediction1=sal_prediction1 ,location1=location1,predictedValue=predictedValue, predictedtitle=predictedtitle,suggestion=suggestion, top=top)

    else:
        flash("Add Technical Skills")
        return redirect(url_for('profile'))
     #### display result ###


                            ############################# END RNN MODEL ##############################

                            ########################## SALARY ANALYSIS ###########################
@app.route('/salary_prediction', methods=['POST', 'GET'])
def salary_prediction():


        stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
                     "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",
                     'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs',
                     'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am',
                     'is',
                     'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
                     'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
                     'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
                     'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                     'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
                     'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
                     'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
                     "should've",
                     'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',
                     "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn',
                     "isn't",
                     'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
                     "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'role',
                     'risk', 'specialist', 'company', 'program', 'multiple', 'process', 'machine', 'data']

        location1 = request.form.get('location')
        title1 = request.form.get('profile')
        location = location1
        title = title1
        data = [[location, title]]
        df1 = pd.DataFrame(data, columns=['Location', 'Title'])

        svm_from_joblib = joblib.load('model_salary.pkl')
        # defining custom stop words of Tfidf
        custom_stop_words = ['role', 'risk', 'specialist', 'company', 'program', 'multiple', 'process', 'machine',
                             'data']
        # stopwords=stopwords.words('english')
        stopwords.extend(custom_stop_words)

        # define a funciton to generate tfidf vector from text data
        def create_tfidf_vec(data):
            tfidf = TfidfVectorizer(stop_words=stopwords, max_df=1000, min_df=1, sublinear_tf=True, ngram_range=(1, 2))
            tfidf.fit(data)
            X_vec = pd.DataFrame(tfidf.transform(data).todense(), columns=tfidf.get_feature_names())
            return X_vec

        col_names = ['analyst', 'app', 'app developer', 'cloud', 'cloud devops', 'devops', 'devops engineer',
                     'engineer',
                     'full', 'full stack', 'learning', 'learning engineer', 'research', 'research analyst', 'scientist',
                     'scientist analyst',
                     'software', 'software developer', 'stack', 'stack developer', 'web', 'web developer', 'Ahmedabad',
                     'Bengaluru',
                     'Chennai', 'Coimbatore', 'Delhi', 'Gurgaon', 'Hyderabad', 'India', 'Indore', 'Jaipur', 'Kochi',
                     'Kolkata',
                     'Mohali', 'Mumbai',
                     'New Delhi', 'Noida', 'Others', 'Pune', 'Surat']

        def single_prediction(var, index):
            var1 = var['Title']
            var_vec = create_tfidf_vec(var1)
            var_vector = np.zeros((1, 41))
            df = pd.DataFrame(var_vector, columns=col_names)
            for i in var_vec.columns:
                if i in df.columns:
                    df[i] = var_vec[i]
                if var['Location'][index] in df.columns:
                    df[var['Location']] = 1
                else:
                    df['Others'] = 1
            prediction = svm_from_joblib.predict(df)
            if prediction == 'High':
                return "4,50,000 - 9,00,000"
            elif prediction == 'Medium':
                return "2,50,000 - 4,50,000"
            else:
                return "Below 2,50,000"

        sal_prediction = single_prediction(df1, 0)
        flash("The salary range for "+ title1 + " at " + location1 + " is " + sal_prediction)
        return redirect(url_for('home'))

                                        #####################  END SALARY ANALYSIS ##########################

                                        ############################# ANALYSIS ##############################

def avg(text):
    if (text.count('-') == 0):
        return int(text)
    else:
        x = text.find('-')
        c = (int(text[:x]) + int(text[x + 1:])) // 2
        return c

@app.route('/A1')
def A1():
    role='Data Scientist and Analyst'
    df3 = pd.read_csv("Final 2.csv")

    df3 = df3.where(df3['Title'] == 'Data Scientist and Analyst')
    df3.dropna(inplace=True)
    s = df3['Location'].size
    l = list(range(0, s))
    df3.set_index(pd.Index(l), inplace=True)
    x = df3['Location'].value_counts()
    dict(x)

    list_of_others = []
    for key, value in x.items():
        if value <= 5:
            list_of_others.append(key)

    for i in range(len(df3)):
        if df3.loc[i, 'Location'] in list_of_others:
            df3.loc[i, 'Location'] = 'Others'

    p = np.array(df3['Title'].value_counts())

    def absolute_value(val):
        a = np.round(val / 100. * p.sum(), 0)
        return a

    y = dict(df3['Location'].value_counts())
    plt.clf()
    plt.pie(y.values(), labels=y.keys(), radius=1.1, autopct=absolute_value)
    plt.title("Distribution of job locations", loc='left', backgroundcolor='black', color='white', fontstyle='italic')

    plt.savefig('static/images/location_graph1.png')

    #graph2
    df1 = pd.read_csv("salfinal.csv")
    df1['Salary'] = df1['Salary'].apply(lambda x: avg(x))
    x = []
    for i in range(len(df1)):
        if (df1['Title'][i] == 'Data Scientist and Analyst'):
            if (df1['Salary'][i] < 3000000):
                x.append(df1['Salary'][i])

    plt.clf()
    plt.hist(x, bins=20)
    plt.ticklabel_format(axis='x', style='plain')
    x_ticks = np.arange(0, 3000000, 250000)
    plt.xticks(x_ticks)
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=15)
    plt.xlabel('Salary')
    plt.ylabel('No. of Jobs')

    plt.savefig('static/images/salary_graph1.png')

    #glist /figure 4

    l1 = ['Python','R Programming Lang','SQL','Spark','Tableau','Hadoop','Statistics']
    return render_template('Graph1.html',role=role,l1 = l1 , name = 'Location',helo1 ='static/images/salary_graph1.png', helo = 'static/images/location_graph1.png')


@app.route('/A2')
def A2():
    role='Machine Learning Engineer'
    df3 = pd.read_csv("Final 2.csv")

    df3 = df3.where(df3['Title'] == 'Machine Learning Engineer')
    df3.dropna(inplace=True)
    s = df3['Location'].size
    l = list(range(0, s))
    df3.set_index(pd.Index(l), inplace=True)
    x = df3['Location'].value_counts()
    dict(x)

    list_of_others = []
    for key, value in x.items():
        if value <= 5:
            list_of_others.append(key)

    for i in range(len(df3)):
        if df3.loc[i, 'Location'] in list_of_others:
            df3.loc[i, 'Location'] = 'Others'

    p = np.array(df3['Title'].value_counts())

    def absolute_value(val):
        a = np.round(val / 100. * p.sum(), 0)
        return a

    y = dict(df3['Location'].value_counts())
    plt.clf()
    plt.pie(y.values(), labels=y.keys(), radius=1.3, autopct=absolute_value)
    plt.title("Distribution of job locations", loc='left', backgroundcolor='black', color='white', fontstyle='italic')

    plt.savefig('static/images/location_graph2')

    # graph2
    df1 = pd.read_csv("salfinal.csv")
    df1['Salary'] = df1['Salary'].apply(lambda x: avg(x))
    x = []
    for i in range(len(df1)):
        if (df1['Title'][i] == 'Machine Learning Engineer'):
            if (df1['Salary'][i] < 3000000):
                x.append(df1['Salary'][i])

    plt.clf()
    plt.hist(x, bins=20)
    plt.ticklabel_format(axis='x', style='plain')
    x_ticks = np.arange(0, 3000000, 250000)
    plt.xticks(x_ticks)
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=15)
    plt.xlabel('Salary')
    plt.ylabel('No. of Jobs')

    plt.savefig('static/images/salary_graph2.png')

    #list 4
    l1 = ['Machine Learning', 'Flask', 'Tensorflow', 'Deep Learning',
     'Matplotlib', 'AI', 'CNN', 'Scikit']
    return render_template('Graph1.html',role=role, l1=l1, name = 'Location',helo1='static/images/salary_graph2.png' ,helo ='static/images/location_graph2.png')

@app.route('/A3')
def A3():
    role='Cloud and DevOps Engineer'
    df3 = pd.read_csv(r"Final 2.csv")

    df3 = df3.where(df3['Title'] == 'Cloud and DevOps Engineer')
    df3.dropna(inplace=True)
    s = df3['Location'].size
    l = list(range(0, s))
    df3.set_index(pd.Index(l), inplace=True)
    x = df3['Location'].value_counts()
    dict(x)

    list_of_others = []
    for key, value in x.items():
        if value <= 5:
            list_of_others.append(key)

    for i in range(len(df3)):
        if df3.loc[i, 'Location'] in list_of_others:
            df3.loc[i, 'Location'] = 'Others'

    p = np.array(df3['Title'].value_counts())

    def absolute_value(val):
        a = np.round(val / 100. * p.sum(), 0)
        return a

    y = dict(df3['Location'].value_counts())
    plt.clf()
    plt.pie(y.values(), labels=y.keys(), radius=1.3, autopct=absolute_value)
    plt.title("Distribution of job locations", loc='left', backgroundcolor='black', color='white', fontstyle='italic')
    plt.savefig('static/images/location_graph3')

    # graph2
    df1 = pd.read_csv("salfinal.csv")
    df1['Salary'] = df1['Salary'].apply(lambda x: avg(x))
    x = []
    for i in range(len(df1)):
        if (df1['Title'][i] == 'Cloud and DevOps Engineer'):
            if (df1['Salary'][i] < 3000000):
                x.append(df1['Salary'][i])

    plt.clf()
    plt.hist(x, bins=20)
    plt.ticklabel_format(axis='x', style='plain')
    x_ticks = np.arange(0, 3000000, 250000)
    plt.xticks(x_ticks)
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=15)
    plt.xlabel('Salary')
    plt.ylabel('No. of Jobs')
    plt.savefig('static/images/salary_graph3.png')

    #list 4
    l1 = ['aws','linux','azure','kubernetes','jenkins','devops','gcp','docker']
    return render_template('Graph1.html',role=role,l1 = l1,  name = 'Location',helo1='static/images/salary_graph3.png' ,helo ='static/images/location_graph3.png')

@app.route('/A4')
def A4():
    role='Full Stack Developer'
    df3 = pd.read_csv("Final 2.csv")

    df3 = df3.where(df3['Title'] == 'Full Stack Developer')
    df3.dropna(inplace=True)
    s = df3['Location'].size
    l = list(range(0, s))
    df3.set_index(pd.Index(l), inplace=True)
    x = df3['Location'].value_counts()
    dict(x)

    list_of_others = []
    for key, value in x.items():
        if value <= 10:
            list_of_others.append(key)

    for i in range(len(df3)):
        if df3.loc[i, 'Location'] in list_of_others:
            df3.loc[i, 'Location'] = 'Others'

    p = np.array(df3['Title'].value_counts())

    def absolute_value(val):
        a = np.round(val / 100. * p.sum(), 0)
        return a

    y = dict(df3['Location'].value_counts())
    plt.clf()
    plt.pie(y.values(), labels=y.keys(), radius=1.3, autopct=absolute_value)
    plt.title("Distribution of job locations", loc='left', backgroundcolor='black', color='white', fontstyle='italic')

    plt.savefig('static/images/location_graph4')

    # graph2
    df1 = pd.read_csv("salfinal.csv")
    df1['Salary'] = df1['Salary'].apply(lambda x: avg(x))
    x = []
    for i in range(len(df1)):
        if (df1['Title'][i] == 'Full Stack Developer'):
            if (df1['Salary'][i] < 3000000):
                x.append(df1['Salary'][i])

    plt.clf()
    plt.hist(x, bins=20)
    plt.ticklabel_format(axis='x', style='plain')
    x_ticks = np.arange(0, 3000000, 250000)
    plt.xticks(x_ticks)
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=15)
    plt.xlabel('Salary')
    plt.ylabel('No. of Jobs')
    plt.savefig('static/images/salary_graph4.png')

    #list 4
    l1 = ['html','css','javascript','rest api','sql','nodejs','mongodb','angularjs']
    return render_template('Graph1.html', role=role,l1 = l1, name = 'Location', helo1='static/images/salary_graph4.png',helo ='static/images/location_graph4.png')

#code which shows distribution of titles in general
@app.route('/A5')
def A5():
    fig = plt.figure()
    df = pd.read_csv('Final 2.csv')
    x = df['Title']
    val = []
    c = dict(df['Title'].value_counts())
    x = c.values()
    y = c.keys()
    p = np.array(df['Title'].value_counts())

    def absolute_value(val):
        a = np.round(val / 100. * p.sum(), 0)
        return a

    plt.clf()
    plt.pie(x, labels=y, radius=1, autopct=absolute_value)
    plt.title("Distribution of job titles", loc='left', backgroundcolor='black', color='white', fontstyle='italic')

    plt.savefig('static/images/dist_of_jobs_general')

    #graph 2
    df1 = pd.read_csv("Final 2.csv")
    df1 = df1.where(df1['Location'] == 'Mumbai')
    df1.dropna(inplace=True)
    d = dict(df1['Title'].value_counts())
    print(d)
    x = d.values()
    y = d.keys()
    q = np.array(df1['Title'].value_counts())

    def absolute_value(val):
        a = np.round(val / 100. * q.sum(), 0)
        return a
    plt.clf()
    my_circle = plt.Circle((0, 0), 0.5, color='white')
    plt.pie(x, labels=y, radius=1.1, autopct=absolute_value, colors=Pastel1_7.hex_colors)
    plt.title("City wise distribution of job titles ", loc='left', backgroundcolor='black', color='white',
              fontstyle='italic')
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.savefig('static/images/dist_of_jobs_general1')

    return render_template('Graph_overall.html',name = 'Location', helo3='static/images/dist_of_jobs_general.png',helo4='static/images/dist_of_jobs_general1.png')

@app.route('/A6')
def A6():
    role='Software Developer'
    df3 = pd.read_csv("Final 2.csv")

    df3 = df3.where(df3['Title'] == 'Software Developer')
    df3.dropna(inplace=True)
    s = df3['Location'].size
    l = list(range(0, s))
    df3.set_index(pd.Index(l), inplace=True)
    x = df3['Location'].value_counts()
    dict(x)

    list_of_others = []
    for key, value in x.items():
        if value <= 10:
            list_of_others.append(key)

    for i in range(len(df3)):
        if df3.loc[i, 'Location'] in list_of_others:
            df3.loc[i, 'Location'] = 'Others'

    p = np.array(df3['Title'].value_counts())

    def absolute_value(val):
        a = np.round(val / 100. * p.sum(), 0)
        return a

    y = dict(df3['Location'].value_counts())
    plt.clf()
    plt.pie(y.values(), labels=y.keys(), radius=1.3, autopct=absolute_value)
    plt.title("Distribution of job locations", loc='left', backgroundcolor='black', color='white', fontstyle='italic')

    plt.savefig('static/images/location_graph6')

    # graph2
    df1 = pd.read_csv("salfinal.csv")
    df1['Salary'] = df1['Salary'].apply(lambda x: avg(x))
    x = []
    for i in range(len(df1)):
        if (df1['Title'][i] == 'Software Developer'):
            if (df1['Salary'][i] < 3000000):
                x.append(df1['Salary'][i])

    plt.clf()
    plt.hist(x, bins=20)
    plt.ticklabel_format(axis='x', style='plain')
    x_ticks = np.arange(0, 3000000, 250000)
    plt.xticks(x_ticks)
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=15)
    plt.xlabel('Salary')
    plt.ylabel('No. of Jobs')
    plt.savefig('static/images/salary_graph6.png')

    #list 4
    l1 = ['java','.net','oops','sql','python','vb.net','mvc']
    return render_template('Graph1.html', role=role,l1=l1,  name = 'Location',helo1='static/images/salary_graph6.png', helo ='static/images/location_graph6.png')


@app.route('/A8')
def A8():
    role='App Developer'
    df3 = pd.read_csv("Final 2.csv")

    df3 = df3.where(df3['Title'] == 'App Developer')
    df3.dropna(inplace=True)
    s = df3['Location'].size
    l = list(range(0, s))
    df3.set_index(pd.Index(l), inplace=True)
    x = df3['Location'].value_counts()
    dict(x)

    list_of_others = []
    for key, value in x.items():
        if value <= 5:
            list_of_others.append(key)

    for i in range(len(df3)):
        if df3.loc[i, 'Location'] in list_of_others:
            df3.loc[i, 'Location'] = 'Others'

    p = np.array(df3['Title'].value_counts())

    def absolute_value(val):
        a = np.round(val / 100. * p.sum(), 0)
        return a

    y = dict(df3['Location'].value_counts())
    plt.clf()
    plt.pie(y.values(), labels=y.keys(), radius=1.3, autopct=absolute_value)
    plt.title("Distribution of job locations", loc='left', backgroundcolor='black', color='white', fontstyle='italic')

    plt.savefig('static/images/location_graph8')

    # graph2
    df1 = pd.read_csv("salfinal.csv")
    df1['Salary'] = df1['Salary'].apply(lambda x: avg(x))
    x = []
    for i in range(len(df1)):
        if (df1['Title'][i] == 'App Developer'):
            if (df1['Salary'][i] < 3000000):
                x.append(df1['Salary'][i])

    plt.clf()
    plt.hist(x, bins=20)
    plt.ticklabel_format(axis='x', style='plain')
    x_ticks = np.arange(0, 3000000, 250000)
    plt.xticks(x_ticks)
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=15)
    plt.xlabel('Salary')
    plt.ylabel('No. of Jobs')
    plt.savefig('static/images/salary_graph8.png')

    #list 4
    l1 = ['java','swift','android sdk','objective c','git','ios','cocoa','json']
    return render_template('Graph1.html', role=role,l1 = l1, name = 'Location',helo1='static/images/salary_graph8.png', helo ='static/images/location_graph8.png')

@app.route('/A9')
def A9():
    role= 'Web Developer'
    df3 = pd.read_csv("Final 2.csv")

    df3 = df3.where(df3['Title'] == 'Web Developer')
    df3.dropna(inplace=True)
    s = df3['Location'].size
    l = list(range(0, s))
    df3.set_index(pd.Index(l), inplace=True)
    x = df3['Location'].value_counts()
    dict(x)

    list_of_others = []
    for key, value in x.items():
        if value <= 20:
            list_of_others.append(key)

    for i in range(len(df3)):
        if df3.loc[i, 'Location'] in list_of_others:
            df3.loc[i, 'Location'] = 'Others'

    p = np.array(df3['Title'].value_counts())

    def absolute_value(val):
        a = np.round(val / 100. * p.sum(), 0)
        return a

    y = dict(df3['Location'].value_counts())
    plt.clf()
    plt.pie(y.values(), labels=y.keys(), radius=1.3, autopct=absolute_value)
    plt.title("Distribution of job locations", loc='left', backgroundcolor='black', color='white', fontstyle='italic')

    plt.savefig('static/images/location_graph9')

    # graph2
    df1 = pd.read_csv("salfinal.csv")
    df1['Salary'] = df1['Salary'].apply(lambda x: avg(x))
    x = []
    for i in range(len(df1)):
        if (df1['Title'][i] == 'Web Developer'):
            if (df1['Salary'][i] < 3000000):
                x.append(df1['Salary'][i])

    plt.clf()
    plt.hist(x, bins=20)
    plt.ticklabel_format(axis='x', style='plain')
    x_ticks = np.arange(0, 3000000, 250000)
    plt.xticks(x_ticks)
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=15)
    plt.xlabel('Salary')
    plt.ylabel('No. of Jobs')
    plt.savefig('static/images/salary_graph9.png')

    l1 = ['html','css','javascript','php','wordpress','bootstrap','git','ajax']
    return render_template('Graph1.html', role=role,l1 = l1 ,name = 'Location', helo1='static/images/salary_graph9.png',helo ='static/images/location_graph9.png')

                    ############################ END ANALYSIS #####################################

                        ##################### Future Analysis ####################
@app.route('/MLE_future')
def MLE_future():
    plt.figure(figsize=(20, 10))
    # The data contains a particular month and number of passengers travelling in that month. In order to read the data as a time series, we have to pass special arguments to the read_csv command:
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
    data = pd.read_csv('ML Future.csv', parse_dates=['Month'], index_col='Month', date_parser=dateparse)
    ts = data['Jobs']
    ts_log = np.log(ts)

    model = ARIMA(ts_log, order=(2, 1, 2))
    results_ARIMA = model.fit(disp=-1)
    results_ARIMA.plot_predict(1, 216)
    x = results_ARIMA.forecast(steps=65)
    y = np.exp(x[0])
    arrcount = []
    arrcount.append(int(sum(y[5:17])))
    arrcount.append(int(sum(y[17:29])))
    arrcount.append(int(sum(y[29:41])))
    arrcount.append(int(sum(y[41:53])))
    arrcount.append(int(sum(y[53:65])))

    plt.savefig("static/images/MLE_future.png")
    return render_template('future_predict.html',arrcount=arrcount, g1 = 'static/images/MLE_future.png', heading="Future Job Predictions for Machine Learning Engineer")

@app.route('/SD_future')
def SD_future():
    plt.figure(figsize=(20, 10))
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
    data = pd.read_csv('Software Future.csv', parse_dates=['Month'], index_col='Month', date_parser=dateparse)
    ts = data['Jobs']
    ts_log = np.log(ts)

    model = ARIMA(ts_log, order=(2, 1, 2))
    results_ARIMA = model.fit(disp=-1)
    results_ARIMA.plot_predict(1, 216)
    x = results_ARIMA.forecast(steps=65)
    y = np.exp(x[0])
    arrcount = []
    arrcount.append(int(sum(y[5:17])))
    arrcount.append(int(sum(y[17:29])))
    arrcount.append(int(sum(y[29:41])))
    arrcount.append(int(sum(y[41:53])))
    arrcount.append(int(sum(y[53:65])))

    plt.savefig("static/images/SD_future.png")
    return render_template('future_predict.html',arrcount=arrcount, g1 = 'static/images/SD_future.png', heading="Future Job Predictions for Software Developer")

                                ##################### End Future Analysis ################

@app.route('/logout')
def logout():
# Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('ID', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
