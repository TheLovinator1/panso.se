FROM postgres:17-bookworm
COPY Docker/*.sql /docker-entrypoint-initdb.d/
RUN chmod a+r /docker-entrypoint-initdb.d/*
