FROM node:20-slim

WORKDIR /app

# pnpmのインストール
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml* ./
RUN pnpm install

COPY . .

EXPOSE 5173
CMD ["pnpm", "run", "dev", "--", "--host"] 