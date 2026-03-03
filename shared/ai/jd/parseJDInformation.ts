import type { H3Event, EventHandlerRequest } from "h3";
import path from "path";

interface IParseConfig {
  fileId: string;
}

export default async function (event: H3Event<EventHandlerRequest>, config: IParseConfig) {
  const { logger } = Logging.client;
  logger.info(`starting parseJDInformation()`);

  logger.info(`reading MultipartFormData()`);
  const formData = await readMultipartFormData(event);
  logger.info(`read MultipartFormData()`);

  if (!formData || formData.length === 0) {
    logger.error("No files uploaded");
    throw createError({
      statusCode: 400,
      statusMessage: "No files uploaded",
    });
  }

  const [url, file] = formData;
  const fileName = `${config.fileId}-${file.filename}`;

  const storage = useStorage("uploads");

  logger.info(`getting setItemRaw() > ${fileName}`);
  await storage.setItemRaw(`${fileName}`, file.data);
  logger.info(`fetched setItemRaw() > ${fileName}`);

  const rootProjectPath = process.cwd();

  const candidateResumePath = path.resolve(rootProjectPath, "public", "uploads", fileName);

  const JD_INFO = url.data.toString("utf-8");

  logger.info(`ending parseJDInformation()`);

  return {
    info: {
      candidateResumePath,
      JD_INFO,
      fileName,
    },
  };
}
