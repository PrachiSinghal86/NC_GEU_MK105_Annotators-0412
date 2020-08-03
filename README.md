# Annotators-0412
# Features
* Job Title Prediction
* Skill Suggestion
* Analysis
* Future Trend Prediction
* Salary Prediction
* Recruiter Profile
# Flow of the Project
**Main.py** is the main file from the website will start. It is a Flask File which will be linked to each and every prediction model and HTML pages.
From the main file we can access each and every feature. First the user will have to make an account and the data will be stored in MySQL.
- Profile
  - After going in profile page the user will have to enter his personal,educational and skills.
  - After that there is an option to predict the job title most suitable for him.
  - Now he be directed to Job Prediction page
  -![alt text](https://github.com/PrachiSinghal86/NC_GEU_MK105_Annotators-0412/blob/master/Screeshots_of_website/profile.jpeg "Profile")
- Job Title Prediction
  - Depending on the work experience, education and skills the title most suitable for him will be predicted.
  - RNN and NLP is used to train the dataset which is extracted from Indeed and Glassdoor.
  - He will also get suggestions of skills which he lack for the that job profile and the top skills for each role is taken from the job description.
  - Depending on his preferred location and title he will get expected salary.
  - He can also directed to job website to  apply for jobs based on the job title predicted.
  -![alt text](https://github.com/PrachiSinghal86/NC_GEU_MK105_Annotators-0412/blob/master/Screeshots_of_website/Job_prediction.jpg "Job Title Prediction")
- Analysis
  - Graphs of various job title are displayed.
  - Skills, Location, Salary are used to plot multiple graphs.
  -![alt text](https://github.com/PrachiSinghal86/NC_GEU_MK105_Annotators-0412/blob/master/Screeshots_of_website/Analysis.jpg "Analysis")
  
- Future Forecast
  - A synthetic data to predict future trend is made using the statistics from various websites.
  - Time Series Analysis of the data is made to get expected number of jobs in a particular profile till 2025.
  -![alt text](https://github.com/PrachiSinghal86/NC_GEU_MK105_Annotators-0412/blob/master/Screeshots_of_website/Future%20Prediction.jpg "Profile")
- Salary Prediction
  - Salary is predicted using Job Title and Location.
  - SVM is used to predict the range.
  -![alt text](https://github.com/PrachiSinghal86/NC_GEU_MK105_Annotators-0412/blob/master/Screeshots_of_website/Salary_prediction.jpg "Profile")
  

## Task Done
- [x] Scrapped Data
- [x] Cleaned Data
- [x] Login Page
- [x] RNN Model
- [x] Analysis Charts
- [x] Skills extraction
- [x] Salary Prediction
- [x] Future Prediction
- [x] Apply Job
