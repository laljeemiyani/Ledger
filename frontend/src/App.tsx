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

  const handleProcess = () => {
    if (selectedFiles.length === 0) return
    setProcessing(true)
    // Simulate processing
    setTimeout(() => {
      setProcessing(false)
      alert(`Processed ${selectedFiles.length} files!`)
    }, 2000)
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
