# EasyNMT prerequisites script install
if [ ! -d "easynmt-env" ];
then
	pip3 install virtualenv
	python3 -m venv easynmt-env
	source ./easynmt-env/bin/activate
	pip install -U easynmt
else
	echo "Virtual environment already exists, skipping..."
fi

