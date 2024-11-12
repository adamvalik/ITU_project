const { defineConfig } = require('@vue/cli-service')

if (typeof defineConfig !== 'function') {
  module.exports = {
    transpileDependencies: [],
    devServer: {
      hot: true,
    },
  }
} else {
  module.exports = defineConfig({
    transpileDependencies: [],
    devServer: {
      hot: true,
    },
  })
}