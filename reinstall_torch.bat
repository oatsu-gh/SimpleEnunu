%~dp0\python-3.9.13-embed-amd64\python.exe -m pip uninstall torch torchaudio torchvision --quiet -y
%~dp0\python-3.9.13-embed-amd64\python.exe -m pip install --upgrade light_the_torch --quiet
%~dp0\python-3.9.13-embed-amd64\python.exe -m ltt install torch --no-chache

PAUSE