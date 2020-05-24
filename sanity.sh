dodgy --ignore paths venv, env
isort -rc --atomic ./
pydocstyle --config=./.pydocstylerc
pycodestyle ./ --config=./.pycodestylerc
