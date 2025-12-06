"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const electron_1 = require("electron");
const child_process_1 = require("child_process");
const path_1 = __importDefault(require("path"));
// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
    electron_1.app.quit();
}
let mainWindow = null;
const createWindow = () => {
    // Create the browser window.
    mainWindow = new electron_1.BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path_1.default.join(__dirname, 'preload.js'),
            nodeIntegration: false,
            contextIsolation: true,
        },
    });
    // Load the index.html of the app.
    if (process.env.VITE_DEV_SERVER_URL) {
        mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL);
        // Open the DevTools.
        mainWindow.webContents.openDevTools();
    }
    else {
        mainWindow.loadFile(path_1.default.join(__dirname, '../dist/index.html'));
    }
    // Clean up
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
};
// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
electron_1.app.on('ready', createWindow);
// Quit when all windows are closed, except on macOS.
electron_1.app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        electron_1.app.quit();
    }
});
electron_1.app.on('activate', () => {
    if (electron_1.BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
// IPC Handlers
electron_1.ipcMain.handle('process-files', async (event, filePaths) => {
    console.log('Processing files:', filePaths);
    return new Promise((resolve, reject) => {
        // Determine paths based on environment
        // In dev: process.cwd() is likely the frontend folder or project root depending on how it's run
        // Using relative paths from __dirname is safer if structure is fixed
        // Path to python exe
        const pythonPath = path_1.default.resolve(__dirname, '../../../venv/Scripts/python.exe');
        // Path to cli script
        const scriptPath = path_1.default.resolve(__dirname, '../../../python/cli.py');
        console.log('Python Path:', pythonPath);
        console.log('Script Path:', scriptPath);
        const pythonProcess = (0, child_process_1.spawn)(pythonPath, [scriptPath, ...filePaths]);
        let resultData = '';
        let errorData = '';
        pythonProcess.stdout.on('data', (data) => {
            resultData += data.toString();
        });
        pythonProcess.stderr.on('data', (data) => {
            errorData += data.toString();
            console.error(`Python Error: ${data}`);
        });
        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Python process exited with code ${code}. Error: ${errorData}`));
                return;
            }
            try {
                const jsonResult = JSON.parse(resultData);
                resolve({ success: true, data: jsonResult });
            }
            catch (e) {
                reject(new Error(`Failed to parse Python output: ${e}. Raw output: ${resultData}`));
            }
        });
    });
});
