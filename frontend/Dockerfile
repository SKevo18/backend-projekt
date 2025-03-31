# stage 1 - build
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies including Vite and Tailwind CSS
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# stage 2 - serve with Nginx
FROM nginx:1.27.4
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]