cd ~/minerva
git pull origin master

pyenv local minerva

pip install -r requirements/common.txt
pip install -r requirements/dev.txt
pip install -e .

sudo systemctl restart minerva.service
