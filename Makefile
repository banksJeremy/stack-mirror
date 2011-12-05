all: bin/pip
	bin/pip install twisted
	bin/pip install lxml

bin/pip:
	virtualenv .

