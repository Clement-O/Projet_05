# Pur Beurre
###### [OpenClassroom](https://openclassrooms.com/fr/) - [Python](https://openclassrooms.com/fr/paths/68-developpeur-dapplication-python) - [Project 05](https://openclassrooms.com/fr/projects/utilisez-les-donnees-publiques-de-lopenfoodfacts)

### REQUIREMENTS
You will need [MySQL 8](https://www.mysql.com/) to get this script working.
You will also need to create a user and give him proper rights (under MySQL 8) :
```mysql
CREATE USER `userpb`@`localhost` IDENTIFIED BY `userpb`;
GRANT ALL PRIVILEGES ON `pur_beurre`.* TO `userpb`@`localhost`;
```
If following user is created with needed rights, the script will create and update the database automatically. 
If not, you have to modify the \'settings.json\' to connect to desired user, password and host.

### HOW TO USE
The script will display a menu and ask you what you want to do.
Following your answer it will propose you other choice(s) and so on. 
All of your choice must be enter according to what is writing, if not it will tell you and ask you again..

###### Classic behaviour :
You type \'FIND\' (or 'f'), then you choose your categories (0 to 9, the ten categories with the most products in).
Once chosen, you will have to choose between 10 random products of said category. If possible, a substitute is picked and you can save it by typing 'SAVE'.
On the menu again, you can type 'SAVED' (or 's') to access all your previously saved products and substitutes.

### F.A.Q
* The first launch can be long, depending of your network and computer, just give it some time, it will inform you of the progress. (It needs to download the products, process them and create the local database).
* You can modify the waited keyword (except the numbers) in the \'settings.json\' , under \"menu\", \"saved\", \"find\", \"update\" and \"quit\".