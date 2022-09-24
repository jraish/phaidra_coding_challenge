FROM python:3.9.4-slim
RUN mkdir -p /app
WORKDIR /app
COPY ./ /app
RUN pip install -r requirements.txt
EXPOSE 8080 9095
CMD [ "python3", "scraper_service.py"]