FROM python:3.7-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]