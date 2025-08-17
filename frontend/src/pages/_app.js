import "@/styles/globals.css";
import Navbar from "@/components/Navbar";
import { Inter } from "next/font/google";
import Head from "next/head";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/router";
import { getCurrentUser, onAuthChange } from "@/lib/auth";

const inter = Inter({
  subsets: ["latin"],
  weight: ["100","200","300","400","500","600","700","800","900"],
});

const PROTECTED = [
  "/libraries",
  "/account",
  "/libraries/*",
  "/papers/*",
];

function isProtected(pathname) {
  for (const p of PROTECTED) {
    if (p.endsWith("/*")) {
      const base = p.slice(0, -2);
      if (pathname === base || pathname.startsWith(base + "/")) return true;
    } else if (pathname === p) {
      return true;
    }
  }
  return false;
}

export default function App({ Component, pageProps }) {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [user, setUser] = useState(null);
  const guardingRef = useRef(false);

  useEffect(() => {
    setUser(getCurrentUser());
    setMounted(true);
    const off = onAuthChange(setUser);
    return off;
  }, []);

  useEffect(() => {
    if (!mounted) return;
    guardCurrent(router.asPath);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mounted]);

  useEffect(() => {
    const onStart = (url) => {
      if (guardingRef.current) return;
      guardingRef.current = true;
      const pathname = url.split("?")[0];
      if (shouldRedirectToLogin(pathname)) {
        const from = encodeURIComponent(pathname);
        router.replace(`/login?from=${from}`);
      }
    };
    const onDone = () => {
      guardingRef.current = false;
    };

    router.events.on("routeChangeStart", onStart);
    router.events.on("routeChangeComplete", onDone);
    router.events.on("routeChangeError", onDone);
    return () => {
      router.events.off("routeChangeStart", onStart);
      router.events.off("routeChangeComplete", onDone);
      router.events.off("routeChangeError", onDone);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  function shouldRedirectToLogin(pathname) {
    if (pathname === "/login") return false;
    const needAuth = isProtected(pathname);
    const isLogged = !!getCurrentUser();
    return needAuth && !isLogged;
  }

  function guardCurrent(currentUrl) {
    const pathname = currentUrl.split("?")[0];
    if (shouldRedirectToLogin(pathname)) {
      const from = encodeURIComponent(pathname);
      router.replace(`/login?from=${from}`);
    }
  }

  if (!mounted) {
    return (
      <div className={`${inter.className} min-h-screen bg-[#161616] text-white`}>
        <Head>
          <title>Papyrus</title>
          <link rel="icon" type="image/png" href="/logo.png" />
        </Head>
        <Navbar />
        <main className="page-app" style={{ opacity: 0.6, padding: 24 }}>
          Loading…
        </main>
      </div>
    );
  }

  return (
    <div className={`${inter.className} min-h-screen bg-[#161616] text-white`}>
      <Head>
        <title>Papyrus</title>
        <link rel="icon" type="image/png" href="/logo.png" />
      </Head>
      <Navbar />
      <main className="page-app">
        <Component {...pageProps} />
      </main>
    </div>
  );
}
