django-angular-seed
===================
This is a "clone and go" seed for django ,angular, and django-rest-framework.

Setup
-----
```
git clone
gem install foreman
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```
Also you will need to create a .env file containing the following
```
ENV=development
PORT=8080
AWS_ACCESS_KEY_ID=<your aws access key>
AWS_SECRET_ACCESS_KEY=<your aws secret key>
AWS_STORAGE_BUCKET_NAME=<your aws bucket>
```

Running
-------
`foreman start`

Note, all python manage.py commands will also probably need to be run through foreman. You should probably make an alias for this.
`foreman run python manage.py ...`

Deploy to Heroku
----------------
This seed also supports deployment to heroku with a few caveats. Static files must be prepared and deployed to S3 before anything will work on Heroku.
You will need to set the variables in your `.env` file on heroku using `heroku config:set VAR=VALUE`.  Make sure to set `ENV=production`.

Once deployed to heroku you need to build you static files:
```
heroku run python manage.py collectstatic
heroku run python manage.py compress
```

