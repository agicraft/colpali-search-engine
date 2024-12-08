FROM node:22.2.0
WORKDIR /app
ARG BASE_URI
ENV BASE_URI=$BASE_URI

COPY ./package*.json .
RUN --mount=type=cache,target=/root/.npm/ npm ci

COPY ./tsconfig*.json ./vite.config.ts ./env.d.ts ./index.html .

ENTRYPOINT ["npm", "run", "dev"]
