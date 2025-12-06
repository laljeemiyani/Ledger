"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const electron_1 = require("electron");
// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
electron_1.contextBridge.exposeInMainWorld('electronAPI', {
    processFiles: (files) => electron_1.ipcRenderer.invoke('process-files', files),
    exportTransactions: (transactions, format) => electron_1.ipcRenderer.invoke('export-transactions', transactions, format),
});
// Type definition for usage in renderer
// This is just the implementation; types need to be declared globally or imported
