const images = require.context("../images", true);
const imagePath = (name) => images(name, true);

export { cytoscape } from "./workflow.js";

require.context("govuk-frontend/govuk/assets");
import { initAll } from "govuk-frontend";
initAll();
