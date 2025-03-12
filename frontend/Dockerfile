# stage 1 - build
# "as builder" = name of the stage, so we can reference it in the next stage
FROM node:18-alpine as builder
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# stage 2 - serve with Nginx
FROM nginx:1.27.4
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
