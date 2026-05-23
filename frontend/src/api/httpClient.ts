import axios from "axios";

import { config } from "../config/environment";

export const httpClient = axios.create({
  baseURL: config.apiBaseUrl,
  timeout: 10_000,
  headers: {
    "Content-Type": "application/json",
  },
});
