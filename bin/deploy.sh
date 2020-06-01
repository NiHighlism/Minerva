cd ~/minerva
git pull origin master

export PATH="$PATH:/usr/bin:/usr/local/bin:/usr/sbin:/home/nihighlism/.pyenv/versions/minerva/bin:/home/nihighlism/.local/bin"
pyenv local minerva

pip install -r requirements/common.txt
pip install -r requirements/dev.txt
pip install -e .

sudo systemctl restart minerva.service
