FROM debian:bookworm
WORKDIR /node12
COPY . ./
RUN apt update && apt upgrade -y && apt install -y \
    vim \
    curl \
    bash \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash \
    && bash -c "source ~/.bashrc && nvm install 12 && nvm use 12"
CMD ["tail", "-f", "/dev/null"]
