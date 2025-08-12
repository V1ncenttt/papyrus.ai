import Link from "next/link";
import { useRouter } from "next/router";
import MenuIcon from "@mui/icons-material/Menu";
import CloseIcon from "@mui/icons-material/Close"; // +++
import styles from "@/styles/Navbar.module.css";
import Image from "next/image";
import { useEffect, useMemo, useRef, useState } from "react";

const nav = [
  { href: "/", label: "Home" },
  { href: "/libraries", label: "My libraries" },
  { href: "/pricing", label: "Pricing" },
];

export default function Navbar() {
  const { pathname, events } = useRouter();
  const isActive = (href) => (href === "/" ? pathname === href : pathname.startsWith(href));

  const containerRef = useRef(null);
  const itemRefs = useRef({});
  const [indicatorStyle, setIndicatorStyle] = useState({ width: 0, x: 0, visible: false });

  const activeHref = useMemo(
    () => nav.find((n) => isActive(n.href))?.href ?? null,
    [pathname]
  );

  useEffect(() => {
    const update = () => {
      if (!containerRef.current || !activeHref) {
        setIndicatorStyle((s) => ({ ...s, visible: false }));
        return;
      }
      const el = itemRefs.current[activeHref];
      if (!el) return;

      const containerRect = containerRef.current.getBoundingClientRect();
      const rect = el.getBoundingClientRect();

      const x = rect.left - containerRect.left - 8;
      const width = rect.width + 16;
      setIndicatorStyle({ width, x, visible: true });
    };

    update();
    window.addEventListener("resize", update);
    const ro = "ResizeObserver" in window ? new ResizeObserver(update) : null;
    if (ro && containerRef.current) ro.observe(containerRef.current);

    return () => {
      window.removeEventListener("resize", update);
      if (ro && containerRef.current) ro.unobserve(containerRef.current);
    };
  }, [activeHref]);

  const [open, setOpen] = useState(false);

  useEffect(() => {
    const close = () => setOpen(false);
    events.on("routeChangeStart", close);
    return () => events.off("routeChangeStart", close);
  }, [events]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e) => e.key === "Escape" && setOpen(false);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <header className={styles.navbarHeader}>
      <nav className={styles.navbarContainer}>
        <Link href="/" className={styles.navbarLogo}>
          <Image src="/logo.png" alt="ScholarMind logo" width={45} height={45} priority />
        </Link>

        <div className={styles.navbarLinks} ref={containerRef}>
          <div
            className={styles.activeIndicator}
            style={{
              opacity: indicatorStyle.visible ? 1 : 0,
              width: indicatorStyle.width,
              transform: `translateY(-50%) translateX(${indicatorStyle.x}px)`,
            }}
            aria-hidden
          />
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              ref={(el) => (itemRefs.current[item.href] = el)}
              className={`${styles.navLink} ${isActive(item.href) ? styles.active : ""}`}
            >
              {item.label}
            </Link>
          ))}
        </div>

        <div className={styles.navbarActions}>
          <Link href="/login" className={styles.loginBtn}>Login</Link>
          <Link href="/get-started" className={styles.getStartedBtn}>Get started</Link>

          <button
            type="button"
            className={styles.mobileMenuBtn}
            aria-expanded={open}
            aria-controls="mobile-panel"
            aria-label="Toggle navigation"
            onClick={() => setOpen((v) => !v)}
          >
            {open ? <CloseIcon fontSize="small" /> : <MenuIcon fontSize="small" />}
          </button>
        </div>
      </nav>

      <div id="mobile-panel" className={`${styles.mobilePanel} ${open ? styles.mobilePanelOpen : ""}`}>
        <div className={styles.mobilePanelInner}>
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`${styles.mobileLink} ${isActive(item.href) ? styles.mobileActive : ""}`}
            >
              {item.label}
            </Link>
          ))}

          <div className={styles.mobileActions}>
            <Link href="/login" className={styles.mobileLogin}>Login</Link>
            <Link href="/get-started" className={styles.mobilePrimary}>Get started</Link>
          </div>
        </div>
      </div>
    </header>
  );
}
