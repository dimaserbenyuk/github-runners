FROM nginx:alpine

# Install AWS CLI v1
RUN apk add --no-cache aws-cli
