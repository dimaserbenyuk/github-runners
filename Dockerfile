# FROM nginx:alpine
# # Install AWS CLI v1
# RUN apk add --no-cache aws-cli

# Stage 1: Build Stage
# Use a specific version of the official Golang image as the base image
FROM golang:1.23-bullseye AS build

# Create a non-root user for running the application
RUN useradd -u 1001 nonroot

# Set the working directory inside the container
WORKDIR /app 

# Copy only the go.mod file to install dependencies efficiently and leverage layer caching
COPY go.mod ./

# Set the GIN_MODE environment variable to release
ENV GIN_MODE=release


# Use cache mounts to speed up the installation of existing dependencies
RUN go mod download

# Copy the entire application source code
COPY . .

# Compile the application during build and statically link the binary
RUN go build \
    -o main

# Stage 2: Deployable Image
# Use a minimal scratch image as the base image for the final image
FROM scratch

# Copy the /etc/passwd file from the build stage to provide non-root user information
COPY --from=build /etc/passwd /etc/passwd

# Copy the compiled application binary from the build stage to the final image
COPY --from=build /app/main /main

# Use the non-root user created in the build stage
USER nonroot

# Expose the port the application will run on
EXPOSE 8080

# Define the command to run the application when the container starts
CMD ["./main"]
# ARG  AMAZON_LINUX_VERSION="2023"
# FROM amazonlinux:${AMAZON_LINUX_VERSION}

# ENV DOCKER_VERSION='26*'


# RUN dnf install -y --allowerasing coreutils curl && \
#     ### install docker
#     dnf install -y --setopt=install_weak_deps=False docker-${DOCKER_VERSION}


# CMD ["/bin/sleep", "36000"]