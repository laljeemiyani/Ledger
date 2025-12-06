import { contextBridge, ipcRenderer } from 'electron';

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  processFiles: (files: string[]) => ipcRenderer.invoke('process-files', files),
  exportTransactions: (transactions: any[], format: string) => ipcRenderer.invoke('export-transactions', transactions, format),
});

// Type definition for usage in renderer
// This is just the implementation; types need to be declared globally or imported
