# docker build -t mgrast/cv-service .

# 
# docker run --rm -p 5000:5000  mgrast/cv-service

# development only:  docker run --rm -p 5000:5000 --name cv-service   mgrast/cv-service gunicorn -w1 -b 0.0.0.0:5000  --error-logfile - --log-level debug --capture-output app:app


FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
