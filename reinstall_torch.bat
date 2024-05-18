@echo Pytorchを再インストールします。数分かかるので気長にお待ちください。
@echo Re-installing PyTotch. Please wait minutes.

nvcc -V

%~dp0\python-3.9.13-embed-amd64\python.exe -m pip uninstall torch torchaudio torchvision --quiet -y
%~dp0\python-3.9.13-embed-amd64\python.exe -m pip install --upgrade light_the_torch --quiet
%~dp0\python-3.9.13-embed-amd64\python.exe -m light_the_torch install torch torchaudio --no-cache

PAUSE