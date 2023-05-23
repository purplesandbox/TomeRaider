# **TomeRaider** #


Introducing TomeRaider, the ultimate solution to relieve you from the overwhelming burden of decision fatigue when choosing your next book to read. Whether you're a parent of a little adventurer or a bookworm seeking your next literary journey, TomeRaider has got you covered. With its features, TomeRaider can help you select age-appropriate books for your little ones, ensuring their reading experiences are both enjoyable and educational. Simply let TomeRaider work its magic, and discover the perfect book tailored to your child's age and interests. Say goodbye to the endless search and let TomeRaider guide you on your literary adventures!

----

TomeRaider is the brainchild of a group of six women with diverse backgrounds who joined forces during their Code First Girls Degree. As their final project, they collaborated and harnessed their strengths to bring the concept of TomeRaider to life. This app is the result of their collective efforts and showcases their dedication and skill in its development.


--------

### **Getting Started** ###


1 - Clone the repo

You can copy the URL from our repo and use the `git clone` command to paste it in your working directory

`$ git clone (add link)`

-need to finish this

Installing / Getting started: 

Minimal requirements:

flask

pprint

tabulate

requests

jsonify

itertools

flask

mysql.connector

urllib.error


to install the minimal requirements 

`$ pip install -r requirements.txt`


### **Configuration** ###

1 - Set up database

Go to `create_tomeraider_db_script.sql` and run the script in your MySQL workbench or your preferred IDE to set up the database

2 - Add your DB password

In `config.py` make sure to add your database password and user name 




### **Try TomeRaider** ###

Run `user_interactions.py` and get books recommended based on the genre, check what you have in your database, or get a random book recommended if you're not sure what to read next. Something you read and liked? You can leave a review and a rating! 

**Features to look out for:** 

1. Search for books by specifying different parameters such as lexile measure (entering values for lexile is optional) and genre
2. Get a random book suggestion by only specifying a genre
3. Look at the database to view their table of to-read books and/or read books.

**Lexile Chart:** 

Lexile levels are a popular method used by schools to measure a student reader's ability. This chart briefly explains the average lexile ranges of different children to help you find an appropriate choice. 
There is not average given for very young children as there is no expectation placed on their reading ability.

<img width="885" alt="Screenshot 2023-05-19 at 13 43 15" src="https://github.com/purplesandbox/CFG_S3_Group4_Project/assets/128521409/2d30dc99-7c7e-48cc-a350-ae0cc9905dd4">




### **Future plans:** ###

With increased time and resources at our disposal, we have exciting plans to enhance TomeRaider even further. One of our upcoming features includes the ability to generate book lists and recommendations in a convenient text file format, making them easily readable and accessible. Additionally, we are working on incorporating a functionality where you can receive these recommendations directly as a text message on your chosen phone number by using *TWILIO*

Furthermore, our immediate priority is to create a user-friendly interface for TomeRaider. We'll be developing a user interface using Flask, HTML, and CSS elements, ensuring that navigating and interacting with the application becomes even more seamless and enjoyable for our users. 


### **Contributing:** ###

You're welcome to contribute to our project! Just work on a different branch from main and submit a pull request. We'll review and implement your code if relevant. 



