# Heat_Wave_Alert_System
Heat Wave Alert System provides heat wave predictions based on various weather parameters, thus sending alerts to its users if Heat Wave is Detected in 'Mumbai' region. It plays a significant role to help reduce the no.of deaths as a result of Heat Strokes by sending timely alerts to registered users. This application provides User-friendly interface where people can register with their mobile numbers, thus receiving alerts when needed which help them take suitable measures to counter Heat Wave.      

This System aims to provide timely alerts to the public based on model's predictions, cautioning them about extreme heat events and provide measures to follow to stay safe.       

# Decision Tree Classifier   
A decision tree classifier was fitted to the training set of a Mumbai's weather data and in-turn used for Heat-Wave predictions on daily basis.      

![Decision_Tree_Classifier](https://github.com/AshishViswas/Heat_Wave_Alert_System/assets/130546401/fe68418f-29bb-4d14-8b1b-c1878c7f52e4)

This ML Algorithm was chosen since it also performs the task of feature selection by only using important features thus reducing model's complexity making it easier to comprehend     

# Dataset 
The jupyter notebook intro.ipynb uses World-weather online API to get weather data for a particular location. 

One can SignUp using the link: https://www.worldweatheronline.com/weather-api/ . After signing Up, they can access the API key which they can use it to get the required data.       

For this Project, only 'Mumbai' data was chosen to minimize the projects complexity
   
The data.py python script uses csv files of weather data and perform operations on it according to this document by government:    
https://mausam.imd.gov.in/responsive/pdf_viewer_css/met2/Chapter%20-2/Chapter%20-2.pdf

Using the python script model.py, a Decision Tree model is trained based on weather data   

# Heat Wave Alert Website    
The code for simple website is available in static and templates folders in this repository.                 
This website lets users subscribe to its heat wave alert service using their mobile number which will be stored in MySQL workbench Database.      
The subscribed users get Heat Wave updates if model predictions are True for Heat Wave based on script running in Flask backend.     
The app.py file was used to define endpoints and MySQL workbench database was used to store the subscribed users.     
A 'cron' job is setup using a background scheduler which sends Heat Wave updates everyday at 10:00 AM, if the model predictions are True.       

# Order of Execution
1. intro.ipynb file to get weather data of 'mumbai' location in csv format
2. data.py file to perform oprations on the data
3. model.py to train the Decision Tree Classifier
4. Download MySQL Workbench and create a Database 'Heat_Wave_Alert_System' and a table 'Subscribers' which can be used to store user data          
  Link to Download MySQL Workbench: https://dev.mysql.com/downloads/workbench/      
5. app.py to run the website

# SMS service   
2Factor API was used to send message notifications. The website to signup: [(https://2factor.in/v3/signup/) ](https://2factor.in/v3/signup/)     

But the SMS will not actually be sent because permissions are needed to send BULK SMS to the public.    

The senders have to first register their templates on TRAI (Telecom Regulatory Authority of India) Portal following which they will be provided with a DLT (Distributed Ledger Technology) SMS API which they can use to send SMS alerts to the public.     

The website for registration : https://www.trai.gov.in/

This project includes the neccessary code for proper implementation except permissions from TRAI    

# Challenges Faced:    
Tried many services which provide SMS/Email integration but SMS services required permissions while Email services required to purchase a subscription, 2Factor was chosen since its implementation was free of charge but for SMS to be sent, the permission has to be taken first and secondly, only 'Mumbai' data was chosen so as to reduce project complexity since choosing more locations require developing separate model for each location based on the location's data which were the two limitation's in the Project.
