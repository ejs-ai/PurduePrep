FROM nikolaik/python-nodejs:python3.12-nodejs21-slim-canary AS base

# Requirements up here to save time using Docker cache
COPY PurduePrep/backend/requirements.txt ./
RUN pip install torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY PurduePrep /PurduePrep

# RUN pip install torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu
# RUN pip install --no-cache-dir -r /PurduePrep/backend/requirements.txt

WORKDIR /PurduePrep/frontend
RUN npm install

EXPOSE 3000
EXPOSE 80
EXPOSE 5000

ENV PYTHONPATH=/PurduePrep

CMD ["sh", "-c", "python3 /PurduePrep/backend/app.py & cd /PurduePrep/frontend && npm run build && npm run start"]