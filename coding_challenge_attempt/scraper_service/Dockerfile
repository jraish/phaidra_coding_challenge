FROM python:3.9.4-slim
RUN groupadd --gid 1000 app && \
    useradd --create-home --gid 1000 --uid 1000 app
RUN mkdir -p /app
WORKDIR /app
COPY ./ /app
RUN pip3 install -r requirements.txt
USER app
ENTRYPOINT ["gunicorn"]
CMD ["app:app"]