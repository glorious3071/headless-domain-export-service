FROM joyzoursky/python-chromedriver:3.7-selenium

WORKDIR /app

COPY app.py /app/

RUN pip install flask robotframework-seleniumwire tldextract

EXPOSE 8000

CMD ["python", "app.py"]