FROM python:3.7

# Working directory
WORKDIR /app

# Copy source code to working directory
COPY . app.py /app/

# Install packages and dependencies from requirements.txt
# hadolint ignore=DL3013
RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt