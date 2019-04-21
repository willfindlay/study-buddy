all:
	pip3 install -r requirements.txt && chmod +x study-buddy.py
install:
	pip3 install -r requirements.txt && cp study-buddy.py /bin/study-buddy && chmod +x /bin/study-buddy
