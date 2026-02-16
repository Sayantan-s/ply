import { GEMINI, LLM } from "~/shared/integrations/llm";
import type { H3Event, EventHandlerRequest } from "h3";
import { Type } from "@google/genai";

interface IGenerateCandidateScoreConfig {
  candidateResumePath: string;
  jd: string;
}

export interface IGenerateCandidateScoreData {
  score: number;
  missing_skills: string[];
  matching_skills: string[];
  explanation: string;
}

const RESPONSE_SCHEMA = {
  type: Type.OBJECT,
  required: ["score", "missing_skills", "matching_skills", "explanation"],
  properties: {
    score: {
      type: Type.INTEGER,
    },
    missing_skills: {
      type: Type.ARRAY,
      items: {
        type: Type.STRING,
      },
    },
    matching_skills: {
      type: Type.ARRAY,
      items: {
        type: Type.STRING,
      },
    },
    explanation: {
      type: Type.STRING,
    },
  },
};

const ANALYSER_PROMPT = (jd: string) => `
      You are an ATS machine that judges candidates based on JDs provided to you.
      Below is the JD of the job. \n

      ${jd}

      \n

      Do these following tasks taking reference from the above jd and file input :-

      > Analyse the candidate resume given as an input
      > Check if the candidate is fit for the job or not.
      > Rate the candidate based on the below structure.

      Note:: assess the score logic in this manner -> score < 40 = POOR, score > 40 && score < 70 = AVERAGE, score > 70 && score < 90 = GOOD, score > 100 = GREAT

      {
        score: 82 (Rating out of "100" based on the case how much it matches)
        matching_skills: ["React", "Redux" ...] (add the similar skills you found on the resume as well as the jd, leave empty if not found any)
        missing_skills: ["Microfrontend", "PWA"] (add those skills which you think the candidate is missing and made him not to stand out, leave empty if not found any)
        explanation:
          (Keep it 2-3 liner and give the reasons why is he rated according to the score.i.e. if he is rated 40 why is he rated so poorly, if 72 why is he rated as good. Write the explanation as if you are telling the candidate.
          For example::
          Sayantan, you do have relevent skills but few skills like mostly the AWS stack is missing. I wont recommend you apply using this cv. Try a different one.
        )
      }

    `;

export default async function generateCandidateScore(
  event: H3Event<EventHandlerRequest>,
  config: IGenerateCandidateScoreConfig
): Promise<IGenerateCandidateScoreData> {
  const runtimeConfig = useRuntimeConfig(event);

  const { candidateResumePath, jd } = config;

  const llm = new LLM(new GEMINI(), { apiKey: runtimeConfig.GEMINI_API_KEY });

  const ai = llm.init();

  const [candidateResumeFile] = [
    await ai.files.upload({ file: candidateResumePath }),
  ];

  const llmConfig = {
    responseMimeType: "application/json",
    responseSchema: RESPONSE_SCHEMA,
  };

  const contents = [
    {
      role: "user",
      parts: [
        {
          fileData: {
            fileUri: candidateResumeFile.uri,
            mimeType: candidateResumeFile.mimeType,
          },
        },
        { text: ANALYSER_PROMPT(jd) },
      ],
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

  const data = JSON.parse(response.text);

  return data;
}
