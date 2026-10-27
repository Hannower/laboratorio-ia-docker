# Build Stage: Compila a aplicação Next.js
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
# Alterado de npm ci para npm install para evitar falhas de dessincronização de lockfile
RUN npm install

COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Production Stage: Executa a aplicação já compilada
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "start"]