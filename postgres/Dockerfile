FROM postgres:15

# Устанавливаем рабочую директорию
WORKDIR /docker-entrypoint-initdb.d

# Копируем скрипты настройки и конфигурационные файлы
COPY init.sql /docker-entrypoint-initdb.d/
COPY postgresql.conf /etc/postgresql/postgresql.conf
COPY pg_hba.conf /etc/postgresql/pg_hba.conf

# Настраиваем конфигурацию PostgreSQL
RUN echo "include '/etc/postgresql/postgresql.conf'" >> /usr/share/postgresql/postgresql.conf.sample

# Переменная окружения для автоматического запуска настроек
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=stocks
