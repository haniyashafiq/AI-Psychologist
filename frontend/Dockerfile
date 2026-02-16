# Frontend Vite Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Expose port
EXPOSE 5173

# Run development server with host binding for Docker
# Note: For production, you'd build and serve static files with nginx
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
