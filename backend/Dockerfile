FROM sconecuratedimages/public-apps:python-3.7.3-alpine3.10
COPY . /backend
RUN mkdir encrypted-backend
COPY generate.sh /generate.sh
RUN bash /generate.sh
RUN cp /backend/keytag /keytag
RUN cp /backend/requirements.txt /requirements.txt
RUN apk add gcc linux-headers musl-dev build-base
RUN pip install -r /requirements.txt
RUN rm -rf /backend
CMD ["python3", "/encrypted-backend/app.py"]
