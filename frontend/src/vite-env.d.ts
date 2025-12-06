export {};

declare global {
  interface Window {
    electronAPI: {
      processFiles: (files: string[]) => Promise<{ success: boolean; data?: any; message?: string }>;
    };
  }
  
  interface File {
    path: string;
  }
}
