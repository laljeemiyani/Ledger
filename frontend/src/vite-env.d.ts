export {};

declare global {
  interface Window {
    electronAPI: {
      processFiles: (files: string[]) => Promise<{ success: boolean; data?: any; message?: string }>;
      exportTransactions: (transactions: any[], format: string) => Promise<{ success: boolean; message: string }>;
    };
  }
  
  interface File {
    path: string;
  }
}
