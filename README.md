VOTING APPLICATION GROUP 1
Installing and Running The Project
clone/download the code
Change directory into the folder cd group-m-voting-app 
Create a virtual environment python -m venv env
Start a Virtual Environment In Windows env\Scripts\activate 
Install the requirements pip install -r requirements.txt
Make Migrations / Instanciate our database python manage.py makemigrations
Run the migrations to create the tables python manage.py migrate
Create a Super User/Admin python manage.py createsuperuser then follow the commands
Start Server python manage.py runserver
