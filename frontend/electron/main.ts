import { app, BrowserWindow, ipcMain } from 'electron';
import { spawn } from 'child_process';
import path from 'path';

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}

let mainWindow: BrowserWindow | null = null;

const createWindow = () => {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // Load the index.html of the app.
  if (process.env.VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL);
    // Open the DevTools.
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }
  
  // Clean up
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
app.on('ready', createWindow);

// Quit when all windows are closed, except on macOS.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// IPC Handlers
ipcMain.handle('process-files', async (event, filePaths: string[]) => {
  console.log('Processing files:', filePaths);
  
  return new Promise((resolve, reject) => {
    // Determine paths based on environment
    // In dev: process.cwd() is likely the frontend folder or project root depending on how it's run
    // Using relative paths from __dirname is safer if structure is fixed
    
    // Path to python exe
    const pythonPath = path.resolve(__dirname, '../../../venv/Scripts/python.exe');
    // Path to cli script
    const scriptPath = path.resolve(__dirname, '../../../python/cli.py');
    
    console.log('Python Path:', pythonPath);
    console.log('Script Path:', scriptPath);
    
    const pythonProcess = spawn(pythonPath, [scriptPath, ...filePaths]);
    
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
      } catch (e) {
        reject(new Error(`Failed to parse Python output: ${e}. Raw output: ${resultData}`));
      }
    });
  });
});
