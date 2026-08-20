FROM python:3.14-slim
WORKDIR /app
RUN useradd -r -u 10001 appuser
COPY pyproject.toml /app/
COPY app /app/app
COPY evals /app/evals
RUN pip install --no-cache-dir .
USER appuser
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
