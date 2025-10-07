import { useEffect, useState } from "react";
import CloseIcon from "@mui/icons-material/Close";
import styles from "@/styles/AddFolderModal.module.css";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";

export default function AddFolderModal({ open, onClose }) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit() {
    console.log(email, password);
  }

  if (!open) return null;

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h2>Add New Folder</h2>
          <button
            className={styles.iconBtn}
            onClick={onClose}
            aria-label="Close"
          >
            <CloseIcon />
          </button>
        </div>

        <form className={styles.card} onSubmit={handleSubmit}>
          <div className={styles.field}>
            <Label htmlFor="name">Folder name</Label>
            <Input
              id="folderName"
              type="text"
              placeholder="Your folder name"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
            />
          </div>

          <div className={styles.field}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Label htmlFor="description">Description</Label>
            </div>
            <Input
              id="folderDesc"
              type="longtext"
              placeholder="The description of your folder"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>
        </form>

        <div className={styles.actions}>
          <button className={styles.secondary} onClick={onClose}>
            Cancel
          </button>
          <button className={styles.primary}>Create</button>
        </div>
      </div>
    </div>
  );
}
