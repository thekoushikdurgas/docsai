import { codebaseFetch } from "@/lib/codebaseClient";

export type CodebaseAnalysisRow = {
  id: string;
  status: string;
  created?: string;
};

export type CodebaseStubResponse = {
  ok: boolean;
  scanner_available: boolean;
  message?: string;
  analysis_id?: string;
  analysis?: unknown | null;
};

export const codebaseService = {
  dashboard: () =>
    codebaseFetch<{
      ok: boolean;
      analyses: CodebaseAnalysisRow[];
      scanner_available: boolean;
      message?: string;
    }>("api/dashboard/"),

  scan: () =>
    codebaseFetch<{
      ok: boolean;
      success?: boolean;
      error?: string;
      scanner_available: boolean;
    }>("api/scan/", { method: "POST" }),

  analysis: (analysisId: string) =>
    codebaseFetch<CodebaseStubResponse>(
      `api/analyses/${encodeURIComponent(analysisId)}/`,
    ),

  files: (analysisId: string) =>
    codebaseFetch<CodebaseStubResponse & { files: unknown[] }>(
      `api/analyses/${encodeURIComponent(analysisId)}/files/`,
    ),

  fileDetail: (analysisId: string, filePath: string) =>
    codebaseFetch<
      CodebaseStubResponse & { file_path: string; content: string | null }
    >(
      `api/analyses/${encodeURIComponent(analysisId)}/files/${filePath
        .split("/")
        .map(encodeURIComponent)
        .join("/")}/`,
    ),

  dependencies: (analysisId: string) =>
    codebaseFetch<CodebaseStubResponse & { dependencies: unknown[] }>(
      `api/analyses/${encodeURIComponent(analysisId)}/dependencies/`,
    ),

  patterns: (analysisId: string) =>
    codebaseFetch<CodebaseStubResponse & { patterns: unknown[] }>(
      `api/analyses/${encodeURIComponent(analysisId)}/patterns/`,
    ),
};
