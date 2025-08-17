import Link from "next/link";
import Head from "next/head";
import styles from "@/styles/error.module.css";

export default function Custom404() {
  return (
    <>
      <Head>
        <title>404 - Page not found</title>
        <meta name="robots" content="noindex" />
      </Head>

      <div className={styles.page}>

        <section className={styles.hero}>
          <h1 className={styles.title}>
            4<span className={styles.titleAccent}>0</span>4
          </h1>
          <p className={styles.subtitle}>
            Oops, this page you are looking for might have been removed, had its name changed or is temporarily unavailable.
          </p>

          <div className={styles.actions}>
            <Link href="/" className={styles.primaryBtn}>
              Back to home
            </Link>
          </div>
        </section>
      </div>
    </>
  );
}
