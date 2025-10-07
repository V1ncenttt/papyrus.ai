import { useEffect, useRef, useState } from "react";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import CloseIcon from "@mui/icons-material/Close";
import styles from "@/styles/UploadModal.module.css";

export default function UploadPdfModal({ open, onClose, onUpload }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    if (!open) return;
    const onKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;

  const pickFile = () => inputRef.current?.click();

  const validate = (f) => {
    if (!f) return false;
    const isPdf =
      f.type === "application/pdf" || /\.pdf$/i.test(f.name || "");
    if (!isPdf) {
      setError("Only PDF files are accepted.");
      return false;
    }
    setError("");
    return true;
  };

  const handleSelected = (e) => {
    const f = e.target.files?.[0];
    if (validate(f)) setFile(f);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);
    const f = e.dataTransfer?.files?.[0];
    if (validate(f)) setFile(f);
  };

  const handleUpload = () => {
    if (!file) return;
    onUpload?.(file);
    onClose();
    setFile(null);
  };

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h2>Add New Paper</h2>
          <button className={styles.iconBtn} onClick={onClose} aria-label="Close">
            <CloseIcon />
          </button>
        </div>

        <div
          className={`${styles.dropzone} ${dragOver ? styles.dragOver : ""}`}
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={pickFile}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && pickFile()}
          aria-label="Upload a PDF or click to browse"
        >
          <CloudUploadIcon className={styles.cloudIcon} />
          <div className={styles.dzTitle}>Upload your PDF file</div>
          <div className={styles.dzSubtitle}>Metadata will be automatically extracted</div>

          <div className={styles.fileBar} onClick={(e) => e.stopPropagation()}>
            <input
              ref={inputRef}
              type="file"
              accept="application/pdf"
              onChange={handleSelected}
              hidden
            />
            <label className={styles.browseBtn} onClick={pickFile}>
              Browse…
            </label>
            <span className={styles.fileName}>
              {file ? file.name : "No file selected."}
            </span>
          </div>
        </div>

        {error && <div className={styles.error}>{error}</div>}

        <div className={styles.actions}>
          <button className={styles.secondary} onClick={onClose}>Cancel</button>
          <button
            className={styles.primary}
            onClick={handleUpload}
            disabled={!file}
          >
            Upload
          </button>
        </div>
      </div>
    </div>
  );
}
