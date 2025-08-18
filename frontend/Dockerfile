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

# Install dependencies, including dev dependencies
RUN npm ci --include=dev

# Copy source code
COPY . .

# Disable telemetry and enable hot reload
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=development
ENV WATCHPACK_POLLING=true
ENV CHOKIDAR_USEPOLLING=true

# Expose port
EXPOSE 3000

# Start development server with hot reload
CMD ["npm", "run", "dev"]
