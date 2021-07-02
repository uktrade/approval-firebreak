const images = require.context("../images", true);
const imagePath = (name) => images(name, true);

import { foo } from "./workflow.js";

console.log(foo);

export { foo };

require.context("govuk-frontend/govuk/assets");
import { initAll } from "govuk-frontend";
initAll();
