# Development Dockerfile for Next.js with hot reload
FROM node:20-alpine

WORKDIR /app

# Install build dependencies for native modules
RUN apk add --no-cache \
    libc6-compat \
    python3 \
    make \
    g++ \
    linux-headers

# Copy package files
COPY package.json package-lock.json* ./

# Create .npmrc for proper architecture
RUN echo "target_arch=arm64" > .npmrc && \
    echo "target_platform=linux" >> .npmrc && \
    echo "target_libc=musl" >> .npmrc

# Clear npm cache and install dependencies
RUN npm cache clean --force
RUN npm ci
RUN npm rebuild

# Copy source code
COPY . .

# Disable telemetry
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=development

# Expose port
EXPOSE 3000

# Start development server with hot reload
CMD ["npm", "run", "dev"]
