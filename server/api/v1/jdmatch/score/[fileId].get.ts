import findJDMatchInfo from "~/shared/ai/jd/findJDMatchInfo";
import { store } from "~/shared/utils/cache";

export default defineEventHandler(async (event) => {
  const fileId = getRouterParam(event, "fileId");
  if (!fileId) throw createError({ statusCode: 400, message: "File ID is required" });
  const data = await findJDMatchInfo({
    fileId: fileId,
    select: "file_id, file_name, jd, score, missing_skills, matching_skills, explanation",
  });
  await store.del(fileId);
  return data;
});
