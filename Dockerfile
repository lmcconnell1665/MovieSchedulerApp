FROM python:3.7

# Working directory
WORKDIR /app

# Copy source code to working directory
COPY . main.py /app/

# Install packages and dependencies from requirements.txt
# hadolint ignore=DL3013
RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 80
EXPOSE 80

# Run the dashboard
CMD ["python", "main.py"]