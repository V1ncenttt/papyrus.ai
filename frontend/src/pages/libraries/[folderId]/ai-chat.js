import { useRouter } from "next/router";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import { folders, papersByFolder } from "@/data/mock";
import layout from "@/styles/Folder.module.css";
import styles from "@/styles/AIChat.module.css"; // nouveau fichier CSS module
import Breadcrumb from "@/components/Breadcrumb";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import SendRoundedIcon from "@mui/icons-material/SendRounded";
import FolderIcon from "@mui/icons-material/Folder";
import InsertDriveFileOutlinedIcon from "@mui/icons-material/InsertDriveFileOutlined";
import AutoAwesomeOutlinedIcon from "@mui/icons-material/AutoAwesomeOutlined";

function AssistantAvatar() {
  return (
    <div className={styles.assistantAvatar}>
      <AutoAwesomeOutlinedIcon
        className={styles.assistantIcon}
        style={{ fontSize: 20 }}
      />
    </div>
  );
}

const EMPTY = [];

export default function AIChat() {
  const router = useRouter();
  const { folderId } = router.query;

  const folder = folders.find((f) => f.id === folderId);
  const papers = useMemo(() => {
    const arr = papersByFolder[folderId];
    return Array.isArray(arr) ? arr : EMPTY;
  }, [folderId]);

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    if (!folder) return;
    const count = papers.length;
    setMessages([
      {
        role: "assistant",
        text: `Hello! I'm your AI research assistant for the “${
          folder.name
        }” collection. I can help you analyze and discuss your ${count} paper${
          count === 1 ? "" : "s"
        } in this collection. Ask me anything!`,
      },
    ]);
  }, [folder, papers]);

  const endRef = useRef(null);
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages.length, isTyping]);

  const onSend = (e) => {
    e.preventDefault();
    const q = input.trim();
    if (!q) return;
    setMessages((m) => [...m, { role: "user", text: q }]);
    setInput("");
    setIsTyping(true);
    setTimeout(() => {
      setMessages((m) => [
        ...m,
        { role: "assistant", text: `You asked: "${q}". (Wire me later)` },
      ]);
      setIsTyping(false);
    }, 900);
  };

  if (!folder) return <div className={layout.page}>Folder not found.</div>;

  return (
    <div className={layout.page}>
      <aside className={layout.sidebar}>
        <div className={layout.sidebarTitle}>FOLDERS</div>
        <ul className={layout.sidebarList}>
          {folders.map((f) => (
            <li key={f.id}>
              <Link
                href={`/libraries/${f.id}`}
                className={`${layout.sidebarItem} ${
                  f.id === folderId ? layout.active : ""
                }`}
              >
                <FolderIcon />
                {f.name}
              </Link>
            </li>
          ))}
        </ul>
      </aside>

      <main className={`${styles.content} ${styles.chatContainer}`}>
        <div className={layout.headerBreadcrumb}>
          <Breadcrumb
            items={[
              { label: "My libraries", href: "/libraries" },
              { label: folder.name, href: `/libraries/${folder.id}` },
              { label: "AI Assistant", href: "" },
            ]}
          />
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

        <Card className={styles.headerCard}>
          <CardContent className={styles.headerCardContent}>
            <InsertDriveFileOutlinedIcon />
            <strong>{folder.name}</strong>
            <span className={styles.headerCount}>
              • {papers.length} paper{papers.length === 1 ? "" : "s"}
            </span>
          </CardContent>
        </Card>

        <div className={styles.chatScroll}>
          {messages.map((m, i) => (
            <div
              key={i}
              className={`${styles.msgRow} ${
                m.role === "user" ? styles.right : styles.left
              }`}
            >
              <div className={styles.msgInner}>
                {m.role === "assistant" && <AssistantAvatar />}
                <div
                  className={`${styles.bubble} ${
                    m.role === "assistant" ? styles.assistant : styles.user
                  }`}
                >
                  {m.text}
                </div>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className={`${styles.msgRow} ${styles.left}`}>
              <div className={styles.msgInner}>
                <Avatar className={styles.avatar}>
                  <AvatarFallback>AI</AvatarFallback>
                </Avatar>
                <div className={`${styles.bubble} ${styles.assistant}`}>
                  <div className={styles.dots}>
                    <i></i>
                    <i></i>
                    <i></i>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={endRef} />
        </div>

        <form onSubmit={onSend} className={styles.inputBar}>
          <textarea
            placeholder={`Ask about papers in ${folder.name}...`}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                onSend(e);
              }
            }}
            className={styles.textArea}
          />
          <Button type="submit" className={styles.sendBtn} aria-label="Send">
            <SendRoundedIcon fontSize="small" />
          </Button>
        </form>
      </main>
    </div>
  );
}
