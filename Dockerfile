# First stage: Build the Go application
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy Go application source code
COPY . .

# Initialize a Go module if not present
RUN go mod init test || true

# Build the Go application
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Second stage: Create a lightweight runtime image
FROM alpine:latest

WORKDIR /root/

# Copy the compiled binary from the builder stage
COPY --from=builder /app/main .

# Define the default command to run the application
CMD ["./main"]
