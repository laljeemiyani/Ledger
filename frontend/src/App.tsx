import { useState } from 'react'
import { FileUpload } from './components/FileUpload'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './components/ui/card'
import { Button } from './components/ui/button'

function App() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const [processing, setProcessing] = useState(false)

  const handleFiles = (files: File[]) => {
    setSelectedFiles(files)
  }

  const handleProcess = async () => {
    if (selectedFiles.length === 0) return
    setProcessing(true)
    
    try {
      if (window.electronAPI) {
        const filePaths = selectedFiles.map(f => f.path)
        const result = await window.electronAPI.processFiles(filePaths)
        console.log("Processing result:", result)
        if (result.success) {
          alert(`Successfully processed ${result.data?.length || 0} files!`)
        } else {
          alert("Error processing files: " + (result.message || "Unknown error"))
        }
      } else {
        // Fallback for browser-only dev (mock)
        console.warn("Electron API not available. Running in mock mode.")
        setTimeout(() => {
          alert(`[MOCK] Processed ${selectedFiles.length} files!`)
        }, 1000)
      }
    } catch (error) {
      console.error("Processing failed:", error)
      alert("Processing failed. See console for details.")
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div className="min-h-screen bg-background p-8 font-sans text-foreground">
      <div className="max-w-4xl mx-auto space-y-8">
        
        <div className="space-y-2">
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl">Ledger</h1>
          <p className="text-xl text-muted-foreground">
            Bank Statement Converter & Analyzer
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Upload Statements</CardTitle>
            <CardDescription>
              Select your bank statements (PDF, CSV, Excel, Images) to begin processing.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <FileUpload 
              onFilesSelected={handleFiles} 
              isProcessing={processing}
            />
            
            {selectedFiles.length > 0 && (
              <div className="flex justify-end pt-4">
                <Button 
                  onClick={handleProcess} 
                  disabled={processing}
                  size="lg"
                  className="w-full sm:w-auto"
                >
                  {processing ? 'Processing...' : `Process ${selectedFiles.length} Files`}
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

      </div>
    </div>
  )
}

export default App
