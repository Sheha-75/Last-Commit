FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# Train the model at image build time so it's baked in.
# (For a hackathon this is fine; for production you'd mount a real model artifact.)
RUN python -m app.data_gen && python -m app.train_model

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
