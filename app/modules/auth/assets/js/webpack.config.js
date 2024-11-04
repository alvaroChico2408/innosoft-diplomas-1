const path = require('path');

module.exports = {
  entry: path.resolve(__dirname, './scripts.js'),
  output: {
    filename: 'auth.bundle.js',
    path: path.resolve(__dirname, '../dist'),
  },
  resolve: {
    fallback: {
    }
  },
  mode: 'development',
};