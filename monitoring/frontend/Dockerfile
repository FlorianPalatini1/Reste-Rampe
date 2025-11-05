FROM nginx:alpine

WORKDIR /usr/share/nginx/html

# Remove default config
RUN rm -f /etc/nginx/conf.d/default.conf

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/monitoring.conf

# Copy frontend
COPY index.html .

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
