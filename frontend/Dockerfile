# Multi-stage build: build with Node, serve with nginx
FROM node:18-slim AS build
ARG SKIP_TRANSCODE=0
WORKDIR /app
COPY frontend/ .

# Copy docker env file - this ensures VITE_API_URL is not set for runtime proxy
RUN cp .env.docker .env.production

# Install ffmpeg and dependencies ONLY if not skipping transcode (for production builds)
RUN if [ "$SKIP_TRANSCODE" = "0" ]; then \
		apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates wget \
		&& rm -rf /var/lib/apt/lists/* \
		|| true; \
	fi

# If a landing.mp4 exists in public/, re-encode it to an H.264 mp4 with faststart for reliable browser playback
# SKIP_TRANSCODE build arg can be set to 1 in dev to skip heavy ffmpeg work
RUN if [ "$SKIP_TRANSCODE" = "1" ]; then \
		echo "Skipping landing video transcode (dev)"; \
	else \
		if [ -f public/landing.mp4 ]; then \
			# produce an H.264 mp4 with faststart
			ffmpeg -y -i public/landing.mp4 -c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 128k -movflags +faststart public/landing_fixed.mp4 && \
			mv public/landing_fixed.mp4 public/landing.mp4 ; \
			# produce a WebM fallback (VP9 + Opus) at moderate quality
			ffmpeg -y -i public/landing.mp4 -c:v libvpx-vp9 -b:v 1M -vf scale=-2:720 -c:a libopus public/landing.webm || true; \
			# generate a poster image at 2 seconds
			ffmpeg -y -ss 2 -i public/landing.mp4 -frames:v 1 -q:v 2 public/landing_poster.jpg || true; \
		fi; \
	fi

# Install deps
RUN npm ci --silent
# ensure CLI bins are executable (some filesystems may lose exec bit)
RUN if [ -d ./node_modules/.bin ]; then chmod -R a+x ./node_modules/.bin || true; fi
# Build production assets
RUN npm run build

FROM nginx:1.25-alpine
# Copy custom nginx config
COPY nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
# Copy built static files from the build stage
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
