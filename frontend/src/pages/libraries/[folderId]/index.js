import { useRouter } from "next/router";
import Link from "next/link";
import { folders, papersByFolder } from "@/data/mock";
import styles from "@/styles/Folder.module.css";
import FolderIcon from "@mui/icons-material/Folder";
import Breadcrumb from "@/components/Breadcrumb";
import Button from "@/components/Button";
import AddIcon from "@mui/icons-material/Add";
import { Separator } from "@/components/ui/separator";
import ChatBubbleIcon from "@mui/icons-material/ChatBubble";
import InsertDriveFileOutlinedIcon from "@mui/icons-material/InsertDriveFileOutlined";
import { useMemo, useState } from "react";
import UploadPDFModal from "@/components/Modal/UploadPDFModal";

const EMPTY = [];

export default function FolderView() {
  const [uploadOpen, setUploadOpen] = useState(false);
  const router = useRouter();
  const { query } = router;
  const { folderId } = query;

  const folder = folders.find((f) => f.id === folderId);
  const papers = useMemo(() => {
    const arr = papersByFolder[folderId];
    return Array.isArray(arr) ? arr : EMPTY;
  }, [folderId]);

  const [search, setSearch] = useState("");
  const norm = (s = "") =>
    s
      .toString()
      .normalize("NFD")
      .replace(/\p{Diacritic}/gu, "")
      .toLowerCase();

  const filtered = useMemo(() => {
    if (!search.trim()) return papers;
    const q = norm(search);
    return papers.filter((p) => norm(p.title).includes(q));
  }, [papers, search]);

  const highlight = (title, q) => {
    if (!q?.trim()) return title;
    const t = title ?? "";
    const makeIdx = () => {
      const a = norm(t);
      const b = norm(q);
      const i = a.indexOf(b);
      return i;
    };
    const i = makeIdx();
    if (i < 0) return t;
    const start = t.slice(0, i);
    const mid = t.slice(i, i + q.length);
    const end = t.slice(i + q.length);

    return (
      <>
        {start}
        <mark
          style={{
            background:
              "linear-gradient(90deg, rgba(255,182,193,0.4) 0%, rgba(255,105,180,0.4) 100%)",
            color: "white",
            padding: "0 2px",
            borderRadius: 4,
          }}
        >
          {mid}
        </mark>
        {end}
      </>
    );
  };

  if (!folder) return <div className={styles.page}>Folder not found.</div>;

  return (
    <div className={styles.page}>
      <aside className={styles.sidebar}>
        <div className={styles.sidebarTitle}>FOLDERS</div>
        <ul className={styles.sidebarList}>
          {folders.map((f) => (
            <li key={f.id}>
              <Link
                href={`/libraries/${f.id}`}
                className={`${styles.sidebarItem} ${
                  f.id === folderId ? styles.active : ""
                }`}
              >
                <FolderIcon />
                {f.name}
              </Link>
            </li>
          ))}
        </ul>
      </aside>

      <main className={styles.content}>
        <div className={styles.headerBreadcrumb}>
          <Breadcrumb
            items={[
              { label: "My libraries", href: "/libraries" },
              { label: folder?.name, href: "" },
            ]}
          />
          <div className={styles.rightCornerBtns}>
            <Button
              startIcon={<ChatBubbleIcon />}
              btnText={"Chat with AI"}
              onClick={() => router.push(`/libraries/${folder.id}/ai-chat`)}
            />
            <Button
              startIcon={<AddIcon />}
              btnText={"Add"}
              onClick={() => setUploadOpen(true)}
            />
          </div>
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

        {papers.length > 0 && (
          <input
            className={styles.search}
            placeholder="Search papers..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        )}

        {papers.length === 0 ? (
          <div className={styles.emptyWrap}>
            <div className={styles.emptyCard}>
              <InsertDriveFileOutlinedIcon style={{ fontSize: 120 }} />
              <h3 className={styles.emptyTitle}>No paper yet</h3>
              <p className={styles.emptySubtitle}>
                Add your first paper to get started with research collection
              </p>
            </div>
          </div>
        ) : filtered.length === 0 ? (
          <div className={styles.emptyWrap}>
            <div className={styles.emptyCard}>
              <h3 className={styles.emptyTitle}>No results</h3>
              <p className={styles.emptySubtitle}>
                Try another keyword or clear the search.
              </p>
            </div>
          </div>
        ) : (
          <div className={styles.table}>
            <div className={styles.thead}>
              <div>Title</div>
              <div>Author</div>
              <div>Year</div>
              <div>Journal</div>
              <div>Type</div>
            </div>
            {filtered.map((p) => (
              <Link key={p.id} href={`/papers/${p.id}`} className={styles.trow}>
                <div className={styles.titleCell}>
                  <div className={styles.paperTitle}>
                    {highlight(p.title, search)}
                  </div>
                  <div className={styles.paperSubtitle}>
                    This is a sample abstract excerpt…
                  </div>
                </div>
                <div>{p.authors}</div>
                <div>{p.year}</div>
                <div className={styles.journalCell}>{p.journal}</div>
                <div>{p.type}</div>
              </Link>
            ))}
          </div>
        )}
        <UploadPDFModal
          open={uploadOpen}
          onClose={() => setUploadOpen(false)}
          onUpload={(file) => {
            console.log("PDF selected:", file);
          }}
        />
      </main>
    </div>
  );
}
