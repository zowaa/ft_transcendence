FROM python:3.11.2

WORKDIR /app

COPY . .

# COPY ["backend", "/app/backend"]
# COPY ["django-env", "/app/django-env"]
# COPY ["users", "/app/users"]
# COPY ["docker-entrypoint.sh", "manage.py", "requirements.txt", "/app/"]

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && apt-get install netcat -y

EXPOSE 8000

# FROM python:3.12-slim

# ENV PYTHONUNBUFFERED 1
# ENV DJANGO_SETTINGS_MODULE=backend.settings

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         git-core \
#         build-essential \
#         binutils \
#         libproj-dev \
#         gdal-bin \
#         supervisor && \
#     rm -rf /var/lib/apt/lists/*

# COPY ./requirements.txt /home/backend/requirements.txt
# RUN mkdir -p /home/backend/media
# WORKDIR /home/backend


# COPY . .

# COPY ["backend", "/app/backend"]
# COPY ["django-env", "/app/django-env"]
# COPY ["users", "/app/users"]
# COPY ["docker-entrypoint.sh", "manage.py", "requirements.txt", "/app/"]

# RUN pip install --upgrade pip
# RUN pip install -r ./requirements.txt



# EXPOSE 8000

# RUN mkdir -p /var/logs/backend


# COPY ./scripts /home/docker/scripts
# COPY ./supervisor-backend.conf /etc/supervisor/conf.d/supervisor-backend.conf

# RUN sed -i 's/\r$//' /home/docker/scripts/boot.sh  && \
#         chmod +x /home/docker/scripts/boot.sh

# ENTRYPOINT /home/docker/scripts/boot.sh

# COPY ./ /home/backend