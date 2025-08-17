import Image from "next/image";
import styles from "@/styles/Home.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <div className={styles.bgGlow} />
      <div className={styles.bgRings} />
      <section className={styles.hero}>
        <div className={styles.badge}>
          New version of Papyrus is out! <a className={styles.badgeLink}>Read more</a>
        </div>

        <h1 className={styles.title}>
          <span>Research</span>
          <span className={styles.titleAccent}>Made Simple</span>
        </h1>

        <p className={styles.subtitle}>
          Upload PDFs, organize collections and chat with AI about research.
          The most elegant way to manage your academic papers.
        </p>

        <div className={styles.ctaRow}>
          <a href="/get-started" className={styles.primaryCta}>Get started</a>
        </div>
      </section>
      <section className={styles.showcase}>
        <Image
          src="/demo-dashboard.png"
          alt="Dashboard preview"
          width={1280}
          height={760}
          className={styles.showcaseCard}
          priority
        />
      </section>
      <section className={styles.spacerSection} />
    </div>
  );
}
