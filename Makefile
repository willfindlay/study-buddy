all:
	pip3 install -r requirements.txt && chmod +x study-buddy.py
install:
	pip3 install -r requirements.txt && mkdir -p /opt/study-buddy; cp *.py /opt/study-buddy && cp ./bin/study-buddy /usr/bin/study-buddy && chmod +x /bin/study-buddy && chmod +x /opt/study-buddy/study-buddy.py
