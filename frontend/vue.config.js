const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8081,              // ton front tourne ici
    host: 'localhost',
    client: { overlay: true },
    proxy: {
      // Toute requête front -> /ask sera proxifiée vers FastAPI
      '^/ask': {
        target: 'http://localhost:8000', // backend FastAPI
        changeOrigin: true,
      },
      // (optionnel) si tu veux accéder à /docs (Swagger) via le même port
      '^/docs': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
