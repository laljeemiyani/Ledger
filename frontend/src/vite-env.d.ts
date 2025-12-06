export {};

declare global {
  interface Window {
    electronAPI: {
      processFiles: (files: string[]) => Promise<{ success: boolean; message: string }>;
    };
  }
}
