dodgy --ignore paths venv env migrations scripts
isort -rc --atomic ./ --skip env
pydocstyle --config=./.pydocstylerc
pycodestyle ./ --config=./.pycodestylerc
