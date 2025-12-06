import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';

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
    
    // Call: python cli.py process file1 file2 ...
    const pythonProcess = spawn(pythonPath, [scriptPath, 'process', ...filePaths]);
    
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

ipcMain.handle('export-transactions', async (event, transactions: any[], format: string) => {
  console.log(`Exporting ${transactions.length} transactions as ${format}`);
  
  if (!mainWindow) return { success: false, message: "No active window" };
  
  const { canceled, filePath } = await dialog.showSaveDialog(mainWindow, {
    title: 'Export Transactions',
    defaultPath: `export_${new Date().toISOString().split('T')[0]}.xml`,
    filters: [{ name: 'XML Files', extensions: ['xml'] }]
  });
  
  if (canceled || !filePath) {
    return { success: false, message: "Export cancelled" };
  }
  
  return new Promise((resolve, reject) => {
    const pythonPath = path.resolve(__dirname, '../../../venv/Scripts/python.exe');
    const scriptPath = path.resolve(__dirname, '../../../python/cli.py');
    
    // Call: python cli.py export --format tally-xml
    const pythonProcess = spawn(pythonPath, [scriptPath, 'export', '--format', format]);
    
    let resultData = '';
    let errorData = '';
    
    pythonProcess.stdout.on('data', (data) => {
      resultData += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      errorData += data.toString();
      console.error(`Python Export Error: ${data}`);
    });
    
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python export process exited with code ${code}. Error: ${errorData}`));
        return;
      }
      
      try {
        const jsonResult = JSON.parse(resultData);
        if (jsonResult.success) {
          const xmlContent = jsonResult.content;
          
          // Write to file
          fs.writeFileSync(filePath, xmlContent, 'utf-8');
          
          resolve({ success: true, message: `Export saved to ${filePath}` });
        } else {
           resolve({ success: false, message: jsonResult.message });
        }
      } catch (e) {
        reject(new Error(`Failed to parse Python export output: ${e}. Raw output: ${resultData}`));
      }
    });
    
    // Send Input Data via Stdin
    pythonProcess.stdin.write(JSON.stringify(transactions));
    pythonProcess.stdin.end();
  });
});
