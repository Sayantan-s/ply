import type {
  CreateJdMatchPayload,
  ResumeUploadData,
  JdMatchStatusData,
  JdMatchAnalysisData,
  JdMatchStreamLine,
  ResponseEnvelope,
} from "../types/api";
import { apiPost, apiGet, streamNdjson } from "./client";

export async function createJdMatch(
  payload: CreateJdMatchPayload,
): Promise<ResponseEnvelope<ResumeUploadData>> {
  const formData = new FormData();

  if (payload.resumeFile) {
    formData.append("resume_file", payload.resumeFile);
  }
  if (payload.resumeUrl) {
    formData.append("resume_url", payload.resumeUrl);
  }
  if (payload.jdInfo) {
    formData.append("jd_info", payload.jdInfo);
  }

  return apiPost<ResumeUploadData>("/api/v1/jdmatch/", formData);
}

export async function* analyzeJdMatch(jdMatchId: string): AsyncGenerator<JdMatchStreamLine> {
  yield* streamNdjson(`/api/v1/jdmatch/${jdMatchId}/analyze`);
}

export async function getJdMatchStatus(
  jdMatchId: string,
): Promise<ResponseEnvelope<JdMatchStatusData>> {
  return apiGet<JdMatchStatusData>(`/api/v1/jdmatch/${jdMatchId}/status`);
}

export async function getJdMatchAnalysis(
  jdMatchId: string,
): Promise<ResponseEnvelope<JdMatchAnalysisData>> {
  return apiGet<JdMatchAnalysisData>(`/api/v1/jdmatch/${jdMatchId}`);
}
