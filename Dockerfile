FROM alpine:latest AS builder
RUN echo "<h1>Hola desde DevOps</h1>" > /usr/share/nginx/html/index.html

FROM nginx:alpine
RUN apk add --no-cache curl
COPY --from=builder /usr/share/nginx/html/index.html /usr/share/nginx/html/
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
