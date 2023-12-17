# Use an official Python runtime as a parent image
FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN python -m venv myvenv

RUN . myvenv/bin/activate

RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["tail", "-f", "/dev/null"]
# CMD ["python", "./cli.py", "--db_host", "db", --db_port, 3306]