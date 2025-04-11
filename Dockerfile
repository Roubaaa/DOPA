FROM node:18-alpine AS frontend-builder

WORKDIR /app

RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    libc6-compat \
    git \
    libpng-dev \
    autoconf \
    automake \
    libtool \
    nasm \
    && npm config set registry https://registry.npmjs.org/ \
    && npm config set strict-ssl false \
    && npm config set fetch-retries 5 \
    && npm config set fetch-retry-mintimeout 20000 \
    && npm config set fetch-retry-maxtimeout 120000 \
    && npm config set cache /tmp/.npm

ENV NODE_OPTIONS="--max-old-space-size=4096"

COPY package*.json ./

RUN npm install --legacy-peer-deps --prefer-offline --no-audit || \
    (echo "First install attempt failed, retrying..." && \
     npm cache clean --force && \
     npm install --legacy-peer-deps --prefer-offline --no-audit)

COPY . .

RUN echo '{"compilerOptions": {"strict": false, "skipLibCheck": true, "noEmit": true, "incremental": true}}' > tsconfig.build.json

RUN NEXT_TELEMETRY_DISABLED=1 npm run build || \
    (echo "Build failed, retrying with clean cache..." && \
     rm -rf .next && \
     NEXT_TELEMETRY_DISABLED=1 npm run build)

FROM node:18-alpine AS frontend

WORKDIR /app

RUN apk add --no-cache \
    curl \
    ca-certificates \
    libpng-dev

COPY --from=frontend-builder /app/.next ./.next
COPY --from=frontend-builder /app/public ./public
COPY --from=frontend-builder /app/package*.json ./
COPY --from=frontend-builder /app/next.config.js ./

RUN npm config set registry https://registry.npmjs.org/ && \
    npm config set strict-ssl false && \
    npm config set cache /tmp/.npm && \
    npm config set legacy-peer-deps true

ENV NODE_OPTIONS="--max-old-space-size=2048"

RUN npm install --production --legacy-peer-deps --prefer-offline --no-audit || \
    (echo "Production install failed, retrying..." && \
     npm cache clean --force && \
     npm install --production --legacy-peer-deps --prefer-offline --no-audit)

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

EXPOSE 3000

CMD ["npm", "start"]

FROM python:3.9-slim AS python-deps

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip config set global.cache-dir /tmp/.pip-cache

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt || (echo "Python dependencies installation failed" && exit 1)

FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY ml_model/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/ml_model/results /tmp/uploads

COPY ml_model/results/2025-04-09_wellpad_model_.keras /app/ml_model/results/

COPY ml_model /app/ml_model

ENV PYTHONPATH=/app
ENV MODEL_PATH=/app/ml_model/results/2025-04-09_wellpad_model_.keras
ENV UPLOAD_FOLDER=/tmp/uploads

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "ml_model.app:app"]