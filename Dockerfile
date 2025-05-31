# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Copy package.json files
COPY package.json ./
COPY fitrack/package.json ./fitrack/
COPY fitrack/package-lock.json ./fitrack/

# Install dependencies at the root level
RUN npm install

# Copy the frontend source code
COPY fitrack/ ./fitrack/

# Build the frontend
WORKDIR /app/fitrack
RUN npm ci && npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy package.json files
COPY package.json ./
COPY fitrack/package.json ./fitrack/

# Install only production dependencies
RUN npm install --only=production
RUN cd fitrack && npm install --only=production

# Copy built assets from build stage
COPY --from=build /app/fitrack/dist ./fitrack/dist
COPY fitrack/server.js ./fitrack/

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose the port
EXPOSE 3000

# Start the server
CMD ["npm", "start"]
