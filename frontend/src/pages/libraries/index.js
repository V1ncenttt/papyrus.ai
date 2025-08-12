import Link from "next/link";
import { folders } from "@/data/mock";
import styles from "@/styles/Libraries.module.css";
import FolderIcon from "@mui/icons-material/Folder";
import Breadcrumb from "@/components/Breadcrumb";
import { Separator } from "@/components/ui/separator";
import Button from "@/components/Button";
import AddIcon from '@mui/icons-material/Add';

export default function Libraries() {

  /* TODO : i18n translation */

  return (
    <div className={styles.page}>
      <aside className={styles.sidebar}>
        <div className={styles.sidebarTitle}>FOLDERS</div>
        <ul className={styles.sidebarList}>
          {folders.map((f) => (
            <Link
              key={f.id}
              href={`/libraries/${f.id}`}
              className={styles.sidebarItem}
            >
              <FolderIcon />
              {f.name}
            </Link>
          ))}
        </ul>
      </aside>

      <main className={styles.content}>
        <div className={styles.headerBreadcrumb}>
          <Breadcrumb items={[{ label: "My libraries", href: "" }]} />
          <Button startIcon={<AddIcon/>} btnText={"Add"}/>
        </div>
        <Separator
          style={{
            height: 1,
            width: "100%",
            background: "rgba(255,255,255,0.12)",
            marginTop: "40px",
            marginBottom: "30px",
          }}
        />

        <div className={styles.foldersGrid}>
          {folders.map((f) => (
            <Link
              key={f.id}
              href={`/libraries/${f.id}`}
              className={styles.folderCard}
            >
              <FolderIcon
                className={styles.folderIcon}
                style={{ fontSize: 80 }}
              />
              <div className={styles.folderName}>{f.name}</div>
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}
