FROM mysql:8.0
ENV MYSQL_DATABASE=interview_db
COPY 01_schema.sql /docker-entrypoint-initdb.d/01_schema.sql
COPY 02_seed.sql /docker-entrypoint-initdb.d/02_seed.sql