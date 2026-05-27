import config from "./codegen";

/** Local API introspection. Start API on :8001 first. */
const localCodegenConfig = {
  ...config,
  schema: "http://127.0.0.1:8001/graphql",
};

export default localCodegenConfig;
