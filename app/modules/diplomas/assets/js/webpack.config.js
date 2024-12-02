module.exports = {
  entry: path.resolve(__dirname, './scripts.js'),
  output: {
    filename: 'diplomas.bundle.js',
    path: path.resolve(__dirname, '../dist'),
  },
  resolve: {
    fallback: {
    }
  },
  mode: 'development',
};
