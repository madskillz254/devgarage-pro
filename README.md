# DEV-GARAGE

Devgarage is a blog website that allows the users to post various blogs about various topics with no restrictions or limitations .

## Getting Started
**[View Code Preview](https://github.com/madskillz254/devgarage)**

## to contribute
fork this repository

clone this repository

``` $ git clone https://github.com/madskillz254/dev-garage-pro ```

 make sure you are at its required level

``` $ cd dev-garage-pro```

 create a virtual environment --these may vary

``` $ python3 -m venv virtual ```

install relevant installations(while in virtual)

``` $ pip install -r requirements.txt ```

create database and link to app

``` $ link database uri to your config.py ```

 make it executable

``` $ create a start.sh and unput secret key etc```

``` $  ./start.sh```


### Prerequisites
Technologies used are listed in the requirements.txt file


## Running the tests
in manage.py change to test instead of development
create test d.b 

``` $ psql```
``` $  create database dev-garage_test with template <original app db name>;```

plac url  in testconfig class
run it

``` $  python3 manage.py test```


## Deployment
change config to production from development in manage.py file
heroku login
heroku create  <app-name>
git add .
git commit -m"initial deployment to heroku"

in config.py add:

class ProdConfig(Config): SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") 

adding required info to heroku
```(virtual)$ heroku config:set MAIL_USERNAME=<YOUR EMAIL ADDRESS>```
```(virtual)$ heroku config:set MAIL_PASSWORD=<YOUR EMAIL PASSWORD> ```
``` heroku addons:create heroku-postgresql --(name of database)  ``` to create a postgresql db on heroku

git push heroku master
``` heroku run python3.6 manage.py db upgrade ``` to create a schema on heroku



## Built With

* [Flask 1.0.2](http://flask.pocoo.org/) - The web framework used 
* [postgresql database](https://www.postgresql.org/) - The database created by postgress 


## Contributing

To contribute 
```fork  the repo```
```git clone https://github.com/madskillz254/dev-garage-pro ```

## Authors
This project is developed and maintained by :
* **DANIEL MUGAMBI** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to corey schafer tutorials


