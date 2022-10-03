const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  // publicPath: "./question-board-saga"に変更したらlocalでも表示されなくなった
  publicPath: "./",
  transpileDependencies: ["vuetify"],
});
