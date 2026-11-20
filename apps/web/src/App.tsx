import { useCallback, useEffect, useRef, useState } from "react";
import {
  agentUrl,
  api,
  browserCapabilities,
  formatBytes,
  getToken,
  type ApkMetadata,
  type Device,
} from "./lib/api";
import "./App.css";

export default function App() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [selectedSerial, setSelectedSerial] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [status, setStatus] = useState<string>("idle");
  const [packages, setPackages] = useState<string[]>([]);
  const [apkMeta, setApkMeta] = useState<ApkMetadata | null>(null);
  const [uploading, setUploading] = useState(false);
  const [installing, setInstalling] = useState(false);
  const [installResult, setInstallResult] = useState<string>("");
  const [confirmInstall, setConfirmInstall] = useState(false);
  const [screenshotUrl, setScreenshotUrl] = useState<string>("");
  const [logcatText, setLogcatText] = useState<string>("");
  const [devicePath, setDevicePath] = useState<string>("/sdcard/Download/upload.bin");
  const [pushFile, setPushFile] = useState<File | null>(null);
  const [pushResult, setPushResult] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const caps = browserCapabilities();

  const refreshDevices = useCallback(async () => {
    setError("");
    setStatus("loading");
    try {
      const data = await api<{ devices: Device[] }>("/api/devices");
      setDevices(data.devices);
      const first = data.devices.find((d) => d.state === "device");
      if (first) {
        setSelectedSerial((prev) => (prev ? prev : first.serial));
      }
      setStatus("ready");
    } catch (e) {
      setError((e as Error).message);
      setStatus("error");
    }
  }, []);

  useEffect(() => {
    refreshDevices();
  }, [refreshDevices]);

  const selectedDevice = devices.find((d) => d.serial === selectedSerial);

  const loadPackages = async () => {
    if (!selectedSerial) return;
    try {
      const data = await api<{ packages: string[] }>(
        `/api/packages?serial=${encodeURIComponent(selectedSerial)}`
      );
      setPackages(data.packages);
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const onFileSelected = async (file: File) => {
    setError("");
    setInstallResult("");
    setApkMeta(null);
    setConfirmInstall(false);
    setUploading(true);
    try {
      const form = new FormData();
      form.append("file", file);
      const token = getToken();
      const res = await fetch(agentUrl("/api/apk/metadata"), {
        method: "POST",
        headers: { "X-DroidStage-Token": token },
        body: form,
      });
      if (!res.ok) {
        const j = await res.json().catch(() => ({}));
        throw new Error(j.detail || `HTTP ${res.status}`);
      }
      const meta = (await res.json()) as ApkMetadata;
      setApkMeta(meta);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setUploading(false);
    }
  };

  const onInstall = async () => {
    if (!apkMeta?.staged_path || !selectedSerial || !confirmInstall) return;
    setInstalling(true);
    setInstallResult("");
    try {
      const result = await api<{ success: boolean; output: string }>(
        "/api/apk/install",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            serial: selectedSerial,
            path: apkMeta.staged_path,
            confirm: true,
          }),
        }
      );
      setInstallResult(result.success ? `Success: ${result.output}` : `Failed: ${result.output}`);
    } catch (e) {
      setInstallResult(`Error: ${(e as Error).message}`);
    } finally {
      setInstalling(false);
    }
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file) onFileSelected(file);
  };

  const takeScreenshot = async () => {
    if (!selectedSerial) return;
    try {
      const token = getToken();
      const res = await fetch(
        agentUrl(`/api/screenshot?serial=${encodeURIComponent(selectedSerial)}&token=${encodeURIComponent(token)}`),
        { headers: { "X-DroidStage-Token": token } }
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setScreenshotUrl((prev) => {
        if (prev) URL.revokeObjectURL(prev);
        return url;
      });
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const fetchLogcat = async () => {
    if (!selectedSerial) return;
    try {
      const data = await api<{ log: string }>(
        `/api/logcat?serial=${encodeURIComponent(selectedSerial)}&lines=200`
      );
      setLogcatText(data.log);
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const doPush = async () => {
    if (!selectedSerial || !pushFile) return;
    setPushResult("");
    try {
      const token = getToken();
      const form = new FormData();
      form.append("serial", selectedSerial);
      form.append("device_path", devicePath);
      form.append("file", pushFile);
      const res = await fetch(agentUrl("/api/files/push"), {
        method: "POST",
        headers: { "X-DroidStage-Token": token },
        body: form,
      });
      if (!res.ok) {
        const j = await res.json().catch(() => ({}));
        throw new Error(j.detail || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setPushResult(data.success ? `Pushed: ${data.output}` : `Failed: ${data.output}`);
    } catch (e) {
      setPushResult(`Error: ${(e as Error).message}`);
    }
  };

  return (
    <div className="app">
      <header className="topbar">
        <h1>DroidStage</h1>
        <span className="badge">pre-alpha</span>
        <button onClick={refreshDevices} disabled={status === "loading"}>
          Refresh devices
        </button>
      </header>

      {!caps.webusb && (
        <div className="alert">
          This browser does not expose WebUSB. Device discovery uses the local agent (adb). Live
          browser streaming is not implemented yet.
        </div>
      )}
      {!caps.webcodecs && (
        <div className="alert">WebCodecs (VideoDecoder) is unavailable; browser video decoding is not supported.</div>
      )}

      <main className="grid">
        <section className="card">
          <h2>Device</h2>
          {status === "loading" && <p>Loading devices…</p>}
          {error && <p className="error">{error}</p>}
          {devices.length === 0 && status === "ready" && <p>No devices found. Connect a phone with USB debugging enabled.</p>}
          <ul className="device-list">
            {devices.map((d) => (
              <li key={d.serial}>
                <label>
                  <input
                    type="radio"
                    name="device"
                    checked={selectedSerial === d.serial}
                    onChange={() => setSelectedSerial(d.serial)}
                  />
                  <span className={`state state-${d.state}`}>{d.state}</span>
                  <strong>{d.metadata?.model || d.model || d.device_name || "Unknown device"}</strong>
                  <small>{d.serial}</small>
                </label>
              </li>
            ))}
          </ul>
          {selectedDevice && (
            <div className="meta">
              <h3>Device info</h3>
              <dl>
                {Object.entries(selectedDevice.metadata || {}).map(([k, v]) => (
                  <div key={k}>
                    <dt>{k}</dt>
                    <dd>{String(v)}</dd>
                  </div>
                ))}
              </dl>
              <button onClick={loadPackages}>List packages</button>
              {packages.length > 0 && (
                <details>
                  <summary>{packages.length} packages</summary>
                  <ul className="packages">
                    {packages.slice(0, 200).map((p) => (
                      <li key={p}>{p}</li>
                    ))}
                  </ul>
                </details>
              )}
            </div>
          )}
        </section>

        <section className="card screen">
          <h2>Live screen</h2>
          <div className="screen-placeholder">
            <p>Live browser-embedded screen streaming is not implemented in this build.</p>
            <p>See docs/adr/0001-physical-device-transport.md for the blocker and plan.</p>
          </div>
        </section>

        <section className="card">
          <h2>Install APK</h2>
          <div
            className="dropzone"
            onDragOver={(e) => e.preventDefault()}
            onDrop={onDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            {uploading ? "Reading APK…" : "Drop an APK here or click to choose"}
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept=".apk"
            hidden
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (f) onFileSelected(f);
            }}
          />
          {apkMeta && (
            <div className="apk-meta">
              <p>
                <strong>{apkMeta.filename}</strong> ({formatBytes(apkMeta.size_bytes)})
              </p>
              {apkMeta.package_name && <p>Package: {apkMeta.package_name}</p>}
              {apkMeta.version_name && <p>Version: {apkMeta.version_name} ({apkMeta.version_code})</p>}
              {apkMeta.min_sdk && <p>Min SDK: {apkMeta.min_sdk}</p>}
              {apkMeta.target_sdk && <p>Target SDK: {apkMeta.target_sdk}</p>}
              {apkMeta.permissions && apkMeta.permissions.length > 0 && (
                <details>
                  <summary>{apkMeta.permissions.length} permissions</summary>
                  <ul>
                    {apkMeta.permissions.map((p) => (
                      <li key={p}>{p}</li>
                    ))}
                  </ul>
                </details>
              )}
              <label className="confirm">
                <input
                  type="checkbox"
                  checked={confirmInstall}
                  onChange={(e) => setConfirmInstall(e.target.checked)}
                />
                I confirm I want to install this APK on the selected device.
              </label>
              <button
                onClick={onInstall}
                disabled={!confirmInstall || installing || !selectedSerial}
              >
                {installing ? "Installing…" : "Install"}
              </button>
            </div>
          )}
          {installResult && <pre className="result">{installResult}</pre>}
        </section>

        <section className="card">
          <h2>Device tools</h2>
          <div className="tools">
            <button onClick={takeScreenshot} disabled={!selectedSerial}>Screenshot</button>
            <button onClick={fetchLogcat} disabled={!selectedSerial}>Logcat (200 lines)</button>
          </div>
          {screenshotUrl && (
            <img src={screenshotUrl} alt="device screenshot" className="screenshot" />
          )}
          <div className="push">
            <h3>Push file</h3>
            <input
              type="file"
              onChange={(e) => setPushFile(e.target.files?.[0] || null)}
            />
            <input
              type="text"
              value={devicePath}
              onChange={(e) => setDevicePath(e.target.value)}
              placeholder="/sdcard/Download/file.bin"
            />
            <button onClick={doPush} disabled={!pushFile || !selectedSerial}>Push</button>
            {pushResult && <pre className="result">{pushResult}</pre>}
          </div>
          {logcatText && <pre className="result">{logcatText}</pre>}
        </section>
      </main>
    </div>
  );
}
