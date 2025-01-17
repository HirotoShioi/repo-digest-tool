import type { paths } from "./schema";
import createClient, { Middleware } from "openapi-fetch";

const middleWare: Middleware = {
  async onResponse({ response }) {
    if (!response.ok) {
      throw new Error(response.statusText);
    }
  },
};

const client = createClient<paths>({
  baseUrl: "http://0.0.0.0:8000",
});

client.use(middleWare);
export default client;