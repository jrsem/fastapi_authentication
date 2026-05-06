FROM python:3.12
WORKDIR /usr/src/personalised_nudges
COPY . ./app


# set env variables
# ENV DATABASE_URL ="postgresql://postgres:animos@localhost/cmrl_db"
# # ENV DATABASE_URL="sqlite:///app/db/post_db.db"
# ENV ACCESS_TOKEN_EXPIRE_MINUTES=30
# ENV ALGORITHM = "HS256" # HMAC with SHA-256
# ENV SALT=hweu77828
# ENV SECRET_KEY=d5ba00efb3b10403949782a6febcba908eca28119ff48586c6f53ec14896243c

COPY requirements.txt requirements.txt


# install dependencies
RUN pip3 install -r requirements.txt
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]