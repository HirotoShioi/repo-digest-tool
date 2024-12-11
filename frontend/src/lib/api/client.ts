import type { paths } from "./schema";
import createClient from "openapi-fetch";

const client = createClient<paths>({
  baseUrl: "http://0.0.0.0:8000",
});

export default client;