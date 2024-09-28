import { defineClientConfig } from "vuepress/client";

import Note from "./components/Note.vue"
import Test from "./components/Test.vue"
import Card from "./components/Card.vue"
import Tense from "./components/Tense.vue"
import Quote from "./components/Quote.vue"

export default defineClientConfig({
  enhance: ({ app, router, siteData }) => {
    app.component("Note", Note);
    app.component("Test", Test);
    app.component("Card", Card);
    app.component("Tense", Tense);
    app.component("Quote", Quote);
  },
});
