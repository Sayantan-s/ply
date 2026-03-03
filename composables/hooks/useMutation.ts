// composables/useMutation.ts

import type { HTTPMethods } from "@upstash/qstash";

export default function <TData = unknown, TError = unknown>(
  url: string,
  method: HTTPMethods = "POST",
  errorCallback?: (error: TError) => string,
): [
  (payload: RequestInit["body"] | Record<string, unknown>) => Promise<TData | null | undefined>,
  {
    loading: Ref<boolean, boolean>;
    error: Ref<string | null, string | null>;
    data: Ref<TData | null, TData | null>;
  },
] {
  const loading = useState("loading", () => false);
  const error = useState<string | null>("error", () => null);
  const data = useState<TData | null>("data", () => null);

  const mutate = async (payload: RequestInit["body"] | Record<string, unknown>) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await $fetch<TData>(url, {
        method,
        body: payload,
      });
      data.value = response as TData;
      return data.value;
    } catch (err) {
      const errorMessage = errorCallback?.(err as TError);
      error.value = errorMessage || "An error occurred";
    } finally {
      loading.value = false;
    }
  };

  return [mutate, { loading, error, data }];
}
