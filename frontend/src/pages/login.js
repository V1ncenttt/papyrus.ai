import styles from "@/styles/Login.module.css";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { mockLogin } from "@/lib/auth";
import GoogleIcon from '@mui/icons-material/Google';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const redirectTo =
    typeof router.query?.redirect === "string" ? router.query.redirect : "/";

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    const res = await mockLogin(email, password);
    if (!res.success) {
      setError(res.message || "Invalid credentials");
      return;
    }
    router.push(redirectTo);
  }

  return (
    <div className={styles.page}>
      <div className={styles.bgGlow} />

      <section className={styles.hero}>
        <h1 className={styles.title}>
          Welcome to <span className={styles.titleAccent}>Papyrus</span>
        </h1>
        <p className={styles.subtitle}>Log in to continue</p>

        <form className={styles.card} onSubmit={handleSubmit}>
          <div className={styles.field}>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="me@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
            />
          </div>

          <div className={styles.field}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Label htmlFor="password">Password</Label>
              <Link href="/forgot-password" className={styles.link}>
                Forgot password?
              </Link>
            </div>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>

          {error && <p className={styles.error}>{error}</p>}

          <div className={styles.footer}>
            <button type="submit" className={styles.primaryBtn}>Login</button>
            <button type="button" className={styles.secondaryBtn}>
              <GoogleIcon style={{fontSize:"20px"}}/> Continue with Google
            </button>
            <p className={styles.link}>
              Don’t have an account?{" "}
              <Link href="/signup" className={styles.link}>Sign up</Link>
            </p>
          </div>
        </form>
      </section>
    </div>
  );
}
