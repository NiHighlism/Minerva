dodgy --ignore paths venv, env, migrations, scripts
isort -rc --atomic ./
pydocstyle --config=./.pydocstylerc
pycodestyle ./ --config=./.pycodestylerc
