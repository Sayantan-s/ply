import analyseIfTextStructureIsAJD from "~/shared/ai/jd/analyseIfTextStructureIsAJD";
import isJdLinkOrDescription from "~/shared/ai/jd/isJdLinkOrDescription";
import { JDMATCH_STATUS } from "~/shared/constants/jd";
import { store } from "~/shared/utils/cache";

export default defineEventHandler(async (event) => {
  const info = await readBody<Awaited<ReturnType<typeof parseJDInformation>>["info"]>(event);

  const storage = useStorage("uploads");

  const { candidateResumePath, JD_INFO: jd_data, fileName } = info;

  const [fileId, ...remainingName] = fileName.split("-");
  try {
    const inputFileName = remainingName.join("-");

    const isJDLink = isJdLinkOrDescription(jd_data);

    const status = isJDLink ? JDMATCH_STATUS.EXTRACTING : JDMATCH_STATUS.ANALYZING;

    await store.set(fileId, { status });

    const jd = isJDLink
      ? await extractJD(event, {
          url: jd_data,
        })
      : await analyseIfTextStructureIsAJD(jd_data);

    await store.set(fileId, {
      status: JDMATCH_STATUS.GENERATING,
      ...(isJDLink ? { data: { jd } } : {}),
    });

    const data = await generateCandidateScore(event, {
      jd,
      candidateResumePath,
    });

    await saveJDMatchInfo({
      jd,
      file_id: fileId,
      file_name: inputFileName,
      ...data,
    });

    await store.set(fileId, {
      status: JDMATCH_STATUS.MATCHED,
      data: { ...data, jd },
    });

    await storage.removeItem(fileName);

    setResponseStatus(event, 200);
  } catch (err) {
    if (err instanceof Error) {
      await store.set(fileId, {
        status: JDMATCH_STATUS.FAILED,
      });
      console.log(err.message);
      throw createError(err);
    }
  }
});
