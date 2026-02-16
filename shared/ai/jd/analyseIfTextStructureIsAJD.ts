import { Type } from "@google/genai";

const JD_ANALYSIS_PROMPT = (text: string) => `
      You are recruiter who can understand the JD of a job.
      You are given a text structure from which you have to understand that it's a JD or not.
      Please anylyse the text and respond in the below format.

      Text Structure:
      ${text}
      \n

      Response Format:

      YES:

      {
        isJD: true
        reason: ""
      }

      \n

      NO:

      {
        isJD: false
        reason: "<Reason why it's not a JD>"
      }
`;

const RESPONSE_SCHEMA = {
  type: Type.OBJECT,
  required: ["isJD", "reason"],
  properties: {
    isJD: {
      type: Type.BOOLEAN,
    },
    reason: {
      type: Type.STRING,
    },
  },
};

export type JDAnalysisResponse = {
  isJD: boolean;
  reason: string;
};

export default async function (text: string) {
  const runtimeConfig = useRuntimeConfig();
  const llm = new LLM(new GEMINI(), { apiKey: runtimeConfig.GEMINI_API_KEY });

  const ai = llm.init();

  const llmConfig = {
    responseMimeType: "application/json",
    responseSchema: RESPONSE_SCHEMA,
  };

  const contents = [
    {
      role: "user",
      parts: [{ text: JD_ANALYSIS_PROMPT(text) }],
    },
  ];

  const response = await ai.models.generateContent({
    model: LLM.model.gemini.FLASH_V25,
    contents: contents,
    config: llmConfig,
  });

  if (!response.text)
    throw createError({
      message: "Failed to generate text",
      statusCode: 400,
    });

  const data: JDAnalysisResponse = JSON.parse(response.text);

  if (!data.isJD)
    throw createError({
      message: data.reason,
      statusCode: 400,
    });

  return text;
}
