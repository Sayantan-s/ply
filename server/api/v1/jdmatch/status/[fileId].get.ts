interface StatusResponse {
  status: JDMATCH_STATUS;
  data: {
    jd?: string;
    score?: number;
    missing_skills?: string[];
    matching_skills?: string[];
    explanation?: string;
  };
}

export default defineEventHandler(async (event) => {
  const fileId = getRouterParam(event, "fileId");
  if (!fileId) throw createError({ statusCode: 404, statusMessage: "File not found!" });
  const value = await store.get<StatusResponse>(fileId);
  if (!value) throw createError({ statusCode: 404, statusMessage: "File not found!" });
  if (value.status === JDMATCH_STATUS.MATCHED) await store.del(fileId);
  if (value.status === JDMATCH_STATUS.FAILED)
    throw createError({
      statusCode: 500,
      statusMessage: `Couldn't generate JD match score`,
    });
  return value;
});
