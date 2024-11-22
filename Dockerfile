# First stage: Build the Go application
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install the correct Go toolchain
RUN GOTOOLCHAIN=auto go install golang.org/dl/go1.23.3@latest && go1.23.3 download

# Copy Go application source code
COPY . .

# # Ensure dependencies are up-to-date
# RUN go mod tidy

# Build the Go application
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Second stage: Create a lightweight runtime image
FROM alpine:latest

WORKDIR /root/

# Copy the compiled binary from the builder stage
COPY --from=builder /app/main .

# Define the default command to run the application
CMD ["./main"]
