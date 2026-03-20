const rawApiBaseUrl = process.env.VUE_APP_API_BASE_URL || "http://localhost:5000";

export const API_BASE_URL = rawApiBaseUrl.replace(/\/$/, "");
