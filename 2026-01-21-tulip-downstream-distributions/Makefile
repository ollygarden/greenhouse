.PHONY: build generate run validate clean

# Build the distribution
build:
	$(MAKE) -C distributions/bonsai build

# Generate sources without compiling (for goreleaser)
generate:
	$(MAKE) -C distributions/bonsai generate

# Run the distribution
run:
	$(MAKE) -C distributions/bonsai run

# Validate the configuration
validate:
	$(MAKE) -C distributions/bonsai validate

# Clean build artifacts
clean:
	$(MAKE) -C distributions/bonsai clean
