export type Device = {
  serial: string;
  state: "device" | "unauthorized" | "offline" | string;
  model?: string | null;
  product?: string | null;
  device_name?: string | null;
  metadata?: Record<string, string>;
};

export type ApkMetadata = {
  filename: string;
  size_bytes: number;
  package_name?: string | null;
  version_name?: string | null;
  version_code?: string | null;
  min_sdk?: string | null;
  target_sdk?: string | null;
  permissions?: string[];
  staged_path?: string;
};

const AGENT_URL = (import.meta.env.VITE_AGENT_URL as string) || "http://127.0.0.1:8787";

export function agentUrl(path: string): string {
  return `${AGENT_URL}${path}`;
}

export function getToken(): string {
  const params = new URLSearchParams(window.location.search);
  const t = params.get("token");
  if (t) {
    localStorage.setItem("droidstage_token", t);
    return t;
  }
  return localStorage.getItem("droidstage_token") || "";
}

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getToken();
  const res = await fetch(agentUrl(path), {
    ...init,
    headers: {
      "X-DroidStage-Token": token,
      ...(init?.headers || {}),
    },
  });
  if (!res.ok) {
    let msg = `HTTP ${res.status}`;
    try {
      const j = await res.json();
      msg = j.detail || msg;
    } catch {
      /* ignore */
    }
    throw new Error(msg);
  }
  return res.json() as Promise<T>;
}

export function formatBytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / (1024 * 1024)).toFixed(1)} MB`;
}

export function browserCapabilities() {
  return {
    webusb: "usb" in navigator,
    webcodecs: typeof (window as any).VideoDecoder !== "undefined",
    webgpu: "gpu" in navigator,
  };
}
