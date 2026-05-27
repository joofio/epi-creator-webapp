
python3 -m venv epi-creator-venv
source epi-creator-venv/bin/activate
pip install -r requirements.txt
sudo cp epi-creator-webapp.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable epi-creator
sudo systemctl start epi-creator
