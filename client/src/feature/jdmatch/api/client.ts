import type { ResponseEnvelope, JdMatchStreamLine } from "../types/api";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

export async function apiPost<T>(
  url: string,
  body: FormData | Record<string, unknown>,
): Promise<ResponseEnvelope<T>> {
  const isFormData = body instanceof FormData;
  const response = await fetch(`${BASE_URL}${url}`, {
    method: "POST",
    headers: isFormData ? undefined : { "Content-Type": "application/json" },
    body: isFormData ? body : JSON.stringify(body),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HTTP ${response.status}: ${text}`);
  }

  return response.json() as Promise<ResponseEnvelope<T>>;
}

export async function apiGet<T>(url: string): Promise<ResponseEnvelope<T>> {
  const response = await fetch(`${BASE_URL}${url}`);

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HTTP ${response.status}: ${text}`);
  }

  return response.json() as Promise<ResponseEnvelope<T>>;
}

export async function* streamNdjson(url: string): AsyncGenerator<JdMatchStreamLine> {
  const response = await fetch(`${BASE_URL}${url}`, { method: "POST" });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HTTP ${response.status}: ${text}`);
  }

  const reader = response.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (line.trim()) {
        yield JSON.parse(line) as JdMatchStreamLine;
      }
    }
  }

  if (buffer.trim()) {
    yield JSON.parse(buffer) as JdMatchStreamLine;
  }
}
