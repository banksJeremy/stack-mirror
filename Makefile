all: bin/pip
	bin/pip install requests
	bin/pip install lxml

bin/pip:
	virtualenv .

