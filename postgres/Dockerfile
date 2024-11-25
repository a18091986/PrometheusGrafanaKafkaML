FROM postgres:15
WORKDIR /docker-entrypoint-initdb.d
COPY init.sql /docker-entrypoint-initdb.d/
COPY postgresql.conf /etc/postgresql/postgresql.conf
COPY pg_hba.conf /etc/postgresql/pg_hba.conf
RUN echo "include '/etc/postgresql/postgresql.conf'" >> /usr/share/postgresql/postgresql.conf.sample
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=stocks
