# Use the official Python image from the Docker Hub
FROM python:3.11.6

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/django

# Install dependencies
COPY requirements.txt /usr/src/django

RUN pip install --upgrade pip && pip install -r requirements.txt

#RUN apt-get update && apt-get install -y netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the project code to the working directory
COPY . /usr/src/django

# Run migrations
RUN python manage.py migrate

COPY entrypoint.sh /usr/src/django/

RUN chmod +x entrypoint.sh

# Expose port 8000 for the Django development server
EXPOSE 8000

# Command to run the entrypoint script
CMD ["./entrypoint.sh"]

# Start the Django development server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]