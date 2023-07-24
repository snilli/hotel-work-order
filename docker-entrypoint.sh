cd /apps

python manage.py migrate
python manage.py init_role
python manage.py runserver 0.0.0.0:3000