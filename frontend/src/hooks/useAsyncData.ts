import { useEffect, useState } from "react";

export function useAsyncData<T>(loader: () => Promise<T>, dependencies: unknown[] = [], intervalMs?: number) {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const result = await loader();
        if (!cancelled) {
          setData(result);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : "Unable to load data");
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    load();
    const timer = intervalMs ? window.setInterval(load, intervalMs) : undefined;
    return () => {
      cancelled = true;
      if (timer) window.clearInterval(timer);
    };
  }, dependencies);

  return { data, isLoading, error };
}

