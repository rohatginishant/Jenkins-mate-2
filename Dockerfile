FROM python:3.8

WORKDIR /app

COPY jenkinsmate-venv app
RUN .\Scripts\activate
RUN pip install -r requirements.txt

CMD [ "python", "-m" , "flask", "run"]









