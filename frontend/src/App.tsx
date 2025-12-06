import { useState } from 'react'
import { FileUpload } from './components/FileUpload'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './components/ui/card'
import { Button } from './components/ui/button'
import { TransactionTable } from './components/TransactionTable'

function App() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const [processing, setProcessing] = useState(false)
  const [results, setResults] = useState<any[]>([])

  const handleFiles = (files: File[]) => {
    setSelectedFiles(files)
    setResults([]) // Reset results when new files selected
  }

  const handleProcess = async () => {
    if (selectedFiles.length === 0) return
    setProcessing(true)
    
    try {
      if (window.electronAPI) {
        const filePaths = selectedFiles.map(f => f.path)
        const response = await window.electronAPI.processFiles(filePaths)
        console.log("Processing result:", response)
        
        if (response.success && response.data) {
          setResults(response.data)
        } else {
          alert("Error processing files: " + (response.message || "Unknown error"))
        }
      } else {
        // Fallback for browser-only dev (mock)
        console.warn("Electron API not available. Running in mock mode.")
        setTimeout(() => {
          setResults([{
            file: "mock.csv",
            status: "success",
            transactions: [
              { date: "2024-01-01", description: "Mock Transaction", debit: 100, credit: 0, balance: 5000 },
              { date: "2024-01-02", description: "Mock Credit", debit: 0, credit: 500, balance: 5500 }
            ]
          }])
        }, 1000)
      }
    } catch (error) {
      console.error("Processing failed:", error)
      alert("Processing failed. See console for details.")
    } finally {
      setProcessing(false)
    }
  }

  const allTransactions = results.flatMap(r => r.transactions || [])

  return (
    <div className="min-h-screen bg-background p-8 font-sans text-foreground">
      <div className="max-w-6xl mx-auto space-y-8">
        
        <div className="space-y-2">
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl">Ledger</h1>
          <p className="text-xl text-muted-foreground">
            Bank Statement Converter & Analyzer
          </p>
        </div>

        <div className="grid gap-8">
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

          {results.length > 0 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <div className="flex items-center justify-between">
                 <h2 className="text-2xl font-bold tracking-tight">Review Data</h2>
                 <div className="flex space-x-2">
                   <Button variant="outline" onClick={() => setResults([])}>Clear Results</Button>
                   <Button onClick={async () => {
                     if (window.electronAPI) {
                       const res = await window.electronAPI.exportTransactions(allTransactions, 'tally-xml')
                       alert(res.message)
                     } else {
                       alert("Mock Export Successful")
                     }
                   }}>
                     Export to Tally XML
                   </Button>
                 </div>
               </div>
               
               {/* Summary Stats or File List could go here */}
               
               <TransactionTable transactions={allTransactions} />
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

export default App
