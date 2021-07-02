const path = require("path");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  context: __dirname,
  entry: {
    main: [
      "./assets/stylesheets/application.scss",
      // this has to come last because webpack is stupid
      "./assets/js/application.js",
    ],
  },
  output: {
    path: path.resolve("./assets/webpack_bundles/"),
    publicPath: "/static/webpack_bundles/",
    filename: "[name]-[contenthash].js",
    library: ["Workflow", "[name]"],
  },

  plugins: [
    new BundleTracker({ filename: "./webpack-stats.json" }),
    new MiniCssExtractPlugin({
      filename: "[name]-[contenthash].css",
      chunkFilename: "[id]-[contenthash].css",
    }),
  ],

  module: {
    rules: [
      // Use asset-modules to handle image assets
      {
        test: /\.(png|jpe?g|gif|woff2?|svg|ico)$/i,
        type: "asset/resource",
        generator: {
          filename: "[name][ext]",
        },
      },

      // Extract compiled SCSS separately from JS
      {
        test: /\.s[ac]ss$/i,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          "css-loader",
          "sass-loader",
        ],
      },
    ],
  },

  resolve: {
    modules: ["node_modules"],
    extensions: [".js", ".scss"],
  },
};
