import type { ResponseEnvelope, ParsedSSEEvent, SSEEventType, SSEEvent } from "../types/api";

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

export async function* streamSSE(url: string): AsyncGenerator<ParsedSSEEvent> {
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
    const blocks = buffer.split("\n\n");
    buffer = blocks.pop() ?? "";

    for (const block of blocks) {
      const trimmed = block.trim();
      if (!trimmed) continue;

      let event: SSEEventType | undefined;
      let data: string | undefined;

      for (const line of trimmed.split("\n")) {
        if (line.startsWith("event: ")) {
          event = line.slice(7) as SSEEventType;
        } else if (line.startsWith("data: ")) {
          data = line.slice(6);
        }
      }

      if (event && data) {
        yield { event, data: JSON.parse(data) as SSEEvent };
      }
    }
  }

  if (buffer.trim()) {
    let event: SSEEventType | undefined;
    let data: string | undefined;

    for (const line of buffer.trim().split("\n")) {
      if (line.startsWith("event: ")) {
        event = line.slice(7) as SSEEventType;
      } else if (line.startsWith("data: ")) {
        data = line.slice(6);
      }
    }

    if (event && data) {
      yield { event, data: JSON.parse(data) as SSEEvent };
    }
  }
}
