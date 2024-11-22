# First stage: Install AWS CLI
FROM alpine:latest AS builder

# Install AWS CLI v1 in the builder stage
RUN apk add --no-cache aws-cli

# Second stage: Final image with Nginx
FROM nginx:alpine

# Copy AWS CLI from builder stage
COPY --from=builder /usr/bin/aws /usr/bin/aws

# Optional: Additional setup for the final stage
# Add your specific configurations, files, or directories
# Example:
# COPY my-nginx-config.conf /etc/nginx/conf.d/default.conf

# Expose the necessary ports
EXPOSE 80
