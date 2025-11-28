# Use the official Agent Zero base image
FROM agent0ai/agent-zero-base:latest

# Set build argument for branch/version if needed
ARG BRANCH=local
ENV BRANCH=$BRANCH

# Copy the filesystem from the repo to the container
COPY ./docker/run/fs/ /

# Copy the current directory (Agent Zero source code) to /git/agent-zero
# This ensures we have the latest code, including the planner plugin
COPY ./ /git/agent-zero

# Install additional requirements from requirements.txt
# This ensures any new dependencies (like updated langchain) are installed
RUN pip install -r /git/agent-zero/requirements.txt

# Note: The planner plugin files are already installed via the COPY instruction above.
# The install_planner_plugin.py script is intended for existing installations.

# Expose necessary ports
EXPOSE 22 80 9000-9009

# Make scripts executable
RUN chmod +x /exe/initialize.sh /exe/run_A0.sh /exe/run_searxng.sh /exe/run_tunnel_api.sh

# Set the working directory
WORKDIR /git/agent-zero

# Default command
CMD ["/exe/initialize.sh", "local"]
