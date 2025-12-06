import React, { useCallback, useState } from 'react';
import { useDropzone, type FileRejection } from 'react-dropzone';
import { UploadCloud, File, X, AlertCircle, FileText, Image as ImageIcon, Table as TableIcon } from 'lucide-react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { cn } from '@/lib/utils';

// Max file size: 50MB
const MAX_SIZE = 50 * 1024 * 1024;

interface FileUploadProps {
  onFilesSelected: (files: File[]) => void;
  className?: string;
  isProcessing?: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onFilesSelected, className, isProcessing }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[], fileRejections: FileRejection[]) => {
    setError(null);
    
    // Handle rejections
    if (fileRejections.length > 0) {
      const firstError = fileRejections[0].errors[0];
      if (firstError.code === 'file-too-large') {
        setError("File is too large. Max size is 50MB.");
      } else if (firstError.code === 'file-invalid-type') {
        setError("Invalid file type. Only PDF, Images, CSV, and Excel are allowed.");
      } else {
        setError(firstError.message);
      }
      return;
    }

    setFiles(prev => {
      const newFiles = [...prev, ...acceptedFiles];
      onFilesSelected(newFiles);
      return newFiles;
    });
  }, [onFilesSelected]);

  const removeFile = (index: number) => {
    setFiles(prev => {
      const newFiles = prev.filter((_, i) => i !== index);
      onFilesSelected(newFiles);
      return newFiles;
    });
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxSize: MAX_SIZE,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg'],
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls']
    },
    disabled: isProcessing
  });

  const getFileIcon = (file: File) => {
    if (file.type.includes('pdf')) return <FileText className="h-8 w-8 text-red-500" />;
    if (file.type.includes('image')) return <ImageIcon className="h-8 w-8 text-blue-500" />;
    if (file.type.includes('spreadsheet') || file.type.includes('csv') || file.type.includes('excel')) return <TableIcon className="h-8 w-8 text-green-500" />;
    return <File className="h-8 w-8 text-gray-500" />;
  };

  return (
    <div className={cn("space-y-4", className)}>
      <div 
        {...getRootProps()} 
        className={cn(
          "border-2 border-dashed rounded-lg p-10 text-center cursor-pointer transition-colors duration-200 ease-in-out flex flex-col items-center justify-center min-h-[200px]",
          isDragActive ? "border-primary bg-primary/10" : "border-muted-foreground/25 hover:border-primary/50",
          isProcessing && "opacity-50 cursor-not-allowed",
          error && "border-destructive bg-destructive/10"
        )}
      >
        <input {...getInputProps()} />
        <div className="bg-primary/10 p-4 rounded-full mb-4">
          <UploadCloud className="h-10 w-10 text-primary" />
        </div>
        {isDragActive ? (
          <p className="text-lg font-medium">Drop the files here ...</p>
        ) : (
          <div className="space-y-2">
            <p className="text-lg font-medium">Drag 'n' drop files here, or click to select</p>
            <p className="text-sm text-muted-foreground">
              Supports PDF, PNG, JPG, CSV, Excel (Up to 50MB)
            </p>
          </div>
        )}
      </div>

      {error && (
        <div className="flex items-center space-x-2 text-destructive bg-destructive/10 p-3 rounded-md text-sm">
          <AlertCircle className="h-4 w-4" />
          <span>{error}</span>
        </div>
      )}

      {files.length > 0 && (
        <div className="grid gap-2">
          {files.map((file, index) => (
            <Card key={`${file.name}-${index}`} className="flex items-center p-3 justify-between">
              <div className="flex items-center space-x-4">
                {getFileIcon(file)}
                <div className="flex flex-col">
                  <span className="text-sm font-medium truncate max-w-[300px]">{file.name}</span>
                  <span className="text-xs text-muted-foreground">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </span>
                </div>
              </div>
              <Button 
                variant="ghost" 
                size="icon" 
                onClick={() => removeFile(index)}
                disabled={isProcessing}
              >
                <X className="h-4 w-4" />
              </Button>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
