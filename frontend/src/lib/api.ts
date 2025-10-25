/**
 * Auto-generated type-safe API client using openapi-fetch
 * Types are automatically synced from the OpenAPI spec
 */
import createClient from "openapi-fetch";
import type { paths } from "@/types/api.d";

// Create the typed client
const client = createClient<paths>({ baseUrl: "http://localhost:5001" });

// Export the client as default
export default client;

