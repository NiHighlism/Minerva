cd ~/minerva
git pull origin master

eval "$( command pyenv init - )"
export PATH="/home/nihighlism/.pyenv/bin:$PATH"
source /home/nihighlism/.zshrc

pyenv "$@"
pyenv local minerva

pip install -r requirements/common.txt
pip install -r requirements/dev.txt
pip install -e .

sudo systemctl restart minerva.service
