import type { H3Event, EventHandlerRequest } from "h3";
import { chromium } from "playwright";
import { z } from "zod";
import { LLM } from "~/shared/integrations/llm";

interface JDConfig {
  url: string;
}

const BROWSING_PROMPT = `
      You are smart machine that understands and extracts contents from webpages.
      Below content should be a JD of a certain job.
      As I mentioned "Should", there can be posibility that you might a find a different webpage which might not be a JD page of example it can be a login page, a shopping card.

      Rules:

      > If you don't find the webpage as JD of job you can throw an error.
      > Extract only the required job description, strictly donot extract unwanted things like about the company etc.

      Strictly follow this json format output::

      Success:

      {
        message: 'SUCCESS',
        data: "<Extracted Content Of the JD>" // for e.g. This is a key role within the Global Deal Desk team, which owns deal strategy, quote-to-cash execution, and pricing operations. You’ll work closely with sales, product, legal, and operations teams to ensure that CPQ changes reflect business prior....
      }

      Error:

      {
        message: 'ERROR',
        data: "<Error Message>" // add error reason in this data property like -> UNKNOWN PAGE, DIFFICULT TO REACH, BLOCKERS CAME UP etc
      }
`;

const ACTION_PROMPT =
  "If any popup / modal / dialog is found on the screen, strictly close it!";

const EXTRACTION_SCHEMA = z.object({
  message: z.string(),
  data: z.string(),
});

const TIMEOUT = 60000;

export default async function (
  event: H3Event<EventHandlerRequest>,
  config: JDConfig
) {
  const { url } = config;
  const runtimeConfig = useRuntimeConfig(event);
  const { logger } = Logging.client;

  const CHROME_PATH = runtimeConfig.CHROME_PATH;
  const API_KEY = runtimeConfig.GEMINI_API_KEY;

  logger.info(`CHROME_PATH -> ${CHROME_PATH}`);
  logger.info(`API_KEY -> ${API_KEY}`);

  const isLocal = process.env.NODE_ENV === "development";

  const chromeExecutablePath = isLocal
    ? CHROME_PATH
    : chromium.executablePath();

  const { page, close } = await browsingAgent({
    apiKey: API_KEY,
    executablePath: chromeExecutablePath,
    model: LLM.model.gemini.FLASH_V25,
  });

  await page.goto(url, { timeout: TIMEOUT });
  logger.info(`naviagted to page -> ${url}`);

  await page.act({ action: ACTION_PROMPT });
  logger.info(`acted on page -> ${url}`);

  const { message, data } = await page.extract<typeof EXTRACTION_SCHEMA>({
    instruction: BROWSING_PROMPT,
    schema: EXTRACTION_SCHEMA,
    modelName: LLM.model.gemini.FLASH_V25,
  });

  logger.info(`message -> ${message}`);
  logger.info(`data -> ${data}`);

  await close();

  if (message === "ERROR")
    throw createError({ statusCode: 400, message: data });

  return data;
}
