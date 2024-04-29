# Use an official Python runtime as a parent image
FROM python:3.9-slim

RUN pip install --no-cache-dir -r requirements.txt

# Run the bot when the container launches
CMD ["python3", "userinfo.py"]
