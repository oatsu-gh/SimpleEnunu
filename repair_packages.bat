@echo Pytorch �� utaupy ���ăC���X�g�[�����܂��B����������̂ŋC���ɂ��҂����������B
@echo Re-installing packages. Please wait some minutes.

nvcc -V

%~dp0\python-3.12.10-embed-amd64\python.exe -m pip install --upgrade utaupy
%~dp0\python-3.12.10-embed-amd64\python.exe -m pip uninstall torch torchaudio torchvision --quiet -y
%~dp0\python-3.12.10-embed-amd64\python.exe -m pip install --upgrade light_the_torch --quiet
%~dp0\python-3.12.10-embed-amd64\python.exe -m light_the_torch install torch torchaudio

PAUSE
