from fabric.api import local


def test():
    local("coverage run manage.py test app")
    local('coverage html --include="app/*" --omit="app/settings*,app/migrations*"')
    local('open htmlcov/index.html')
