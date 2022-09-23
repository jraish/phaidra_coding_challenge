FROM python:3.9.4-slim
RUN mkdir -p /app
WORKDIR /app
COPY ./ /app
RUN pip install -r requirements.txt
EXPOSE 8080 9095
# CMD ["gunicorn", "-b", "127.0.0.1:8080", "-w", "1", "scraper_service:app"]
CMD [ "python3", "scraper_service.py"]