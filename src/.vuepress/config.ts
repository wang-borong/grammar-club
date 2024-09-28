import { defineUserConfig } from "vuepress";

import theme from "./theme.js";

export default defineUserConfig({
  base: "/grammar-club/",

  lang: "zh-CN",
  title: "语法俱乐部",
  description: "语法俱乐部——旋元佑（修订版）",

  theme,

  // 和 PWA 一起启用
  // shouldPrefetch: false,

  // TODO or REMOVE
  head: [
    //...

    // import an external script
    ["script", { src: "//unpkg.com/heti/umd/heti-addon.min.js" }],
    // add a script
    [
      "script",
      {},
      `\
        const heti = new Heti('.heti');
        heti.autoSpacing(); // 自动进行中西文混排美化和标点挤压
      `,
    ],
    // add an external CSS
    ["link", { rel: "stylesheet", href: "//unpkg.com/heti/umd/heti.min.css" }],
    // add a style
    // We don't recommend this, you should prefer to use .vuepress/style/index.scss
    [
      "style",
      {},
      `\
        /* your style here */
      `,
    ],
  ],
});

