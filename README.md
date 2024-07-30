<p align="center">
  <img src="https://github.com/purplesandbox/CFG_S3_Group4_Project/assets/128521409/807b9f08-9602-4881-8155-2aa1675bcc44"/>
</p>


# **TomeRaider** #


----


Introducing TomeRaider, the ultimate solution to relieve you from the overwhelming burden of decision fatigue when choosing your next book to read. Whether you're the parent of a little adventurer or a bookworm seeking your next literary journey, TomeRaider has got you covered. With its features, TomeRaider can help you select age-appropriate books for your little ones, ensuring their reading experiences are both enjoyable and educational. Simply let TomeRaider work its magic, and discover the perfect book tailored to your child's age and interests. Say goodbye to the endless search and let TomeRaider guide you on your literary adventures!



TomeRaider is the brainchild of a group of six women with diverse backgrounds who joined forces during their Code First Girls Degree. As their final project, they collaborated and harnessed their strengths to bring the concept of TomeRaider to life. This app is the result of their collective efforts and showcases their dedication and skill in its development.


--------
### **Getting Started** ###
-----


Clone the repo

```
git clone https://github.com/purplesandbox/CFG_S3_Group4_Project.git
```

---
**Minimal requirements:**

----

In order to run the program you will need to have the following installed: 

- tabulate==0.9.0
- requests==2.31.0
- jsonify==0.5
- mysql-connector-python==8.0.33
- responses==0.23.1
- python-dotenv==1.0.0


Your system should install the minimal requirements automatically, but if needed run
 
```
pip install -r requirements.txt
```
---
### **Configuration** ###
---

1 - Set up database

From the src folder open the Database folder and use`create_tomeraider_db_script.sql` to create your database

 - Optional: use the `populate_db.sql` file to add entries to the db, if you wish to pre-populate it with sample data

2 - Add your DB password

In `config.py` make sure to add your database password and username 

3 - Create `.env` file and generate your own API keys:
- Create `.env` file in the project folder and paste the following into the `.env` file:<br />
        `X-RapidAPI-Key=`<br />
        `X-RapidAPI-Host=book-finder1.p.rapidapi.com`<br />
        
- Go to the https://rapidapi.com/dfskGT/api/book-finder1/ - signup and login so that `X-RapidAPI-Key` can be generated (you can find it under Header Parameters), copy the key and paste it in the .env file like this: `X-RapidAPI-Key=XXXXXXXXXXXXXXXXXX`

4 - Run programme

Open and run `main.py` from the src folder

---
### **Try TomeRaider** ###
---

Run `main.py` and get books recommended based on the genre, check what you have in your database, or get a random book recommended if you're not sure what to read next. Something you read and liked? You can leave a review and a rating! 

**Features to look out for:** 

1. Search for books by specifying different parameters such as lexile measure (entering values for lexile is optional) and genre
2. Get a random book suggestion by only specifying a genre
3. Look at the database to view their table of to-read books and/or read books
4. Add a book to your read list and leave a review and/or a rating

**Lexile Chart:** 

Lexile levels are a popular method used by schools to measure a student reader's ability. This chart briefly explains the average lexile ranges of different children to help you find an appropriate choice. 
There is no average given for very young children as there is no expectation placed on their reading ability.

<img width="885" alt="Screenshot 2023-05-19 at 13 43 15" src="https://github.com/purplesandbox/CFG_S3_Group4_Project/assets/128521409/2d30dc99-7c7e-48cc-a350-ae0cc9905dd4">



---
### **Future plans:** ###
---

With increased time and resources at our disposal, we have exciting plans to enhance TomeRaider even further. Our immediate priority is to create a user-friendly and beautiful graphical interface for TomeRaider. We'll be developing a user interface using the Flask framework ensuring that navigation and interaction with the programme becomes even more seamless and enjoyable for our users. 

We intend to use a cloud based hosting service to deploy our app on the world wide web, that also entails moving the currently locally served data base to a cloud based database service. Further development foresees adding user accounts and authentication so that users can interact with their own book lists created in the database.

---
### **The team** ##
---

. [Maryam Asaria](https://github.com/MaryamA123)

. [Mun-Wei Kan](https://github.com/mwkan)

. [Caitlin Oddy](https://github.com/Catreeney2)

. [Sophie Philipps](https://github.com/SaPhilipps)

. [Sabine Lazuhina](https://github.com/purplesandbox)

. [Tania Alessi](https://github.com/16tales)

---
### **Contributing:** ###
---

You're welcome to contribute to our project! Just work on a different branch from main and submit a pull request. We'll review and implement your code if relevant. 
