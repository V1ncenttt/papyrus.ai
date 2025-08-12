import "@/styles/globals.css";
import Navbar from "@/components/Navbar";
import { Inter } from "next/font/google";
import Head from "next/head";

const inter = Inter({
  subsets: ["latin"],
  weight: [
    "100", // Thin
    "200", // Extra Light
    "300", // Light
    "400", // Regular
    "500", // Medium
    "600", // Semi Bold
    "700", // Bold
    "800", // Extra Bold
    "900", // Black
  ],
});

export default function App({ Component, pageProps }) {
  return (
    <div className={`${inter.className} min-h-screen bg-[#161616] text-white`}>
      <Head>
        <title>ScholarMind</title>
        <link rel="icon" type="image/png" href="/logo.png" />
      </Head>
      <Navbar />
      <main className="page-app">
        <Component {...pageProps} />
      </main>
    </div>
  );
}
