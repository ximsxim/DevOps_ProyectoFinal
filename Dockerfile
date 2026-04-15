FROM alpine:latest AS builder
RUN mkdir -p /tmp/html && echo "<h1>Hola desde DevOps</h1>" > /tmp/html/index.html

FROM nginx:alpine
RUN apk add --no-cache curl
COPY --from=builder /tmp/html/index.html /usr/share/nginx/html/
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
