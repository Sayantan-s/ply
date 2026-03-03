interface JDMatchInfo {
  fileId?: string;
  select: string;
}

export interface JDMatchInfoResponse {
  file_id: string;
  jd: string;
  score: number;
  missing_skills: string[];
  matching_skills: string[];
  explanation: string;
  file_name: string;
}

export default async function (info: JDMatchInfo): Promise<JDMatchInfoResponse> {
  const supabase = useSupabaseServer();

  let query = supabase.from("jd_match_dtl").select(info.select);

  if (info.fileId) query = query.eq("file_id", info.fileId);

  const { data, error } = await query.single();

  if (error)
    throw createError({
      statusCode: 500,
      statusMessage: "Failed to fetch data from Supabase",
    });

  if (!data)
    throw createError({
      statusCode: 404,
      statusMessage: "No data found",
    });

  return data as unknown as JDMatchInfoResponse;
}
