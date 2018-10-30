FROM python3:latest
LABEL maintainer="Ron Rivera"

ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/

ENV DJANGO_ENV playground
ENV DJANGO_DB_NAME gatekeeper
ENV DJANGO_DB_HOST gatekeeper-playground
ENV DJANGO_DB_PORT 5432
ENV DJANGO_DB_USER postgres
ENV DJANGO_DB_PASSWORD postgres
ENV DJANGO_MANAGEPY_MIGRATE true

EXPOSE 8080

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["python", "gatekeeper/manage.py", "runserver", "0.0.0.0:8080"]
