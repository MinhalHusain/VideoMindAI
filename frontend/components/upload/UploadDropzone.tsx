"use client";

import { useState, useCallback, useRef } from "react";
import { UploadCloud, FileVideo, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

const ALLOWED_TYPES = ["video/mp4", "video/quicktime", "video/x-msvideo", "video/x-matroska"];
const ALLOWED_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv"];

interface UploadDropzoneProps {
  onFileSelect: (file: File) => void;
  isLoading?: boolean;
}

export function UploadDropzone({ onFileSelect, isLoading = false }: UploadDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const validateAndProcessFile = (file: File) => {
    setError(null);

    // Validate file type
    if (!ALLOWED_TYPES.includes(file.type) && !ALLOWED_EXTENSIONS.some(ext => file.name.toLowerCase().endsWith(ext))) {
      setError("Invalid file type. Please upload an MP4, MOV, AVI, or MKV video.");
      return;
    }

    onFileSelect(file);
  };

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (isLoading) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      validateAndProcessFile(file);
      e.dataTransfer.clearData();
    }
  }, [isLoading, onFileSelect]);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      validateAndProcessFile(file);
      // Reset input so the same file can be selected again if needed
      e.target.value = '';
    }
  };

  const handleClick = () => {
    if (!isLoading && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="w-full space-y-4">
      <div
        onClick={handleClick}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={cn(
          "relative flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed p-12 transition-all duration-200",
          isDragging 
            ? "border-violet-500 bg-violet-500/10 dark:bg-violet-500/5" 
            : "border-border bg-card hover:border-violet-500/50 hover:bg-accent/50",
          isLoading && "pointer-events-none opacity-60"
        )}
      >
        <input 
          type="file" 
          ref={fileInputRef}
          onChange={handleFileInput}
          accept={ALLOWED_EXTENSIONS.join(",")} 
          className="hidden" 
        />
        
        <div className="flex h-20 w-20 items-center justify-center rounded-full bg-violet-100 dark:bg-violet-900/20 mb-6">
          <UploadCloud className={cn(
            "h-10 w-10 text-violet-600 dark:text-violet-400 transition-transform duration-300",
            isDragging && "scale-110"
          )} />
        </div>
        
        <div className="space-y-2 text-center">
          <h3 className="text-xl font-semibold tracking-tight text-foreground">
            {isDragging ? "Drop your video here" : "Click or drag video to upload"}
          </h3>
          <p className="text-sm text-muted-foreground">
            Supported formats: MP4, MOV, AVI, MKV
          </p>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 rounded-lg bg-destructive/15 p-4 text-sm text-destructive">
          <AlertCircle className="h-4 w-4 shrink-0" />
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}
