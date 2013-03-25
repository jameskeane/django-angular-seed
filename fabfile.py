from fabric.api import local


def test():
    local("python manage.py test app --liveserver=localhost:8082,8090-8100,9000-9200,7041")
    local('coverage html --include="app/*" --omit="app/settings*,app/migrations*"')
    local('open htmlcov/index.html')
