import { useState } from "react";
import styles from "@/styles/Pricing.module.css";

const plans = [
  {
    id: "free",
    name: "Starter",
    blurb: "Get started with the basics",
    priceMonthly: 0,
    priceYearly: 0,
    cta: "Get started",
    highlight: false,
    features: [
      "Up to 50 PDFs",
      "Unlimited collections",
      "Local search",
      "Basic export",
    ],
    limits: "Personal use only",
  },
  {
    id: "pro",
    name: "Pro",
    blurb: "For daily research work",
    priceMonthly: 12,
    priceYearly: 108,
    cta: "Upgrade to Pro",
    highlight: true,
    features: [
      "1,000+ PDFs",
      "Priority AI chat",
      "Citation extraction",
      "Advanced tags & filters",
      "Multi-device sync",
    ],
    limits: "Single user",
  },
  {
    id: "team",
    name: "Team",
    blurb: "Collaboration for labs and teams",
    priceMonthly: 29,
    priceYearly: 276,
    cta: "Contact sales",
    highlight: false,
    features: [
      "Unlimited members",
      "Shared workspaces",
      "Roles & permissions",
      "SAML SSO",
      "Priority support",
    ],
    limits: "Up to 10,000 PDFs",
  },
];

export default function PricingPage() {
  const [yearly, setYearly] = useState(true);

  return (
    <div className={styles.page}>
      <div className={styles.bgGlow} />
      <div className={styles.bgRings} />

      <section className={styles.hero}>
        <h1 className={styles.title}>
          Simple pricing <br/>for{" "}
          <span className={styles.titleAccent}>everyone</span>
        </h1>
        <p className={styles.subtitle}>
          Choose a plan that scales with your research. Cancel anytime.
        </p>

        <div className={styles.billingToggle}>
          <button
            className={`${styles.toggleBtn} ${!yearly ? styles.active : ""}`}
            onClick={() => setYearly(false)}
          >
            Monthly
          </button>
          <button
            className={`${styles.toggleBtn} ${yearly ? styles.active : ""}`}
            onClick={() => setYearly(true)}
          >
            Yearly
          </button>
        </div>
      </section>

      <section className={styles.grid}>
        {plans.map((p) => (
          <div
            key={p.id}
            className={`${styles.card} ${
              p.highlight ? styles.cardHighlight : ""
            }`}
          >
            {p.highlight && (
              <div className={styles.mostPopular}>Most popular</div>
            )}

            <div className={styles.cardHeader}>
              <h3 className={styles.planName}>{p.name}</h3>
              <p className={styles.planBlurb}>{p.blurb}</p>
              <div className={styles.priceRow}>
                {p.priceMonthly === 0 ? (
                  <span className={styles.priceFree}>Free</span>
                ) : (
                  <>
                    <span className={styles.price}>
                      ${yearly ? p.priceYearly : p.priceMonthly}
                    </span>
                    <span className={styles.per}>
                      {yearly ? " /year" : " /month"}
                    </span>
                  </>
                )}
              </div>
              {yearly && p.priceMonthly !== 0 && (
                <div className={styles.subPrice}>
                  ${Math.round(p.priceYearly / 12)}/mo billed yearly
                </div>
              )}
            </div>

            <ul className={styles.features}>
              {p.features.map((f, i) => (
                <li key={i} className={styles.featureItem}>
                  <span className={styles.check} aria-hidden>
                    ✓
                  </span>
                  {f}
                </li>
              ))}
            </ul>

            <div className={styles.cardFooter}>
              <a href="#" className={styles.primaryBtn}>
                {p.cta}
              </a>
              <div className={styles.limitNote}>{p.limits}</div>
            </div>
          </div>
        ))}
      </section>

      <section className={styles.faq}>
        <h2 className={styles.faqTitle}>Frequently asked questions</h2>
        <div className={styles.faqGrid}>
          <div>
            <h3>Can I cancel anytime?</h3>
            <p>
              Yes. All subscriptions are commitment-free. You keep access until
              the end of your billing period.
            </p>
          </div>
          <div>
            <h3>Do you offer student discounts?</h3>
            <p>Yes, 30% off Pro with a valid student ID.</p>
          </div>
          <div>
            <h3>How is PDF storage handled?</h3>
            <p>
              Files are encrypted at rest and in transit. You can export them
              anytime.
            </p>
          </div>
          <div>
            <h3>Does the Team plan include dedicated support?</h3>
            <p>
              Yes, you get a priority support channel and guided onboarding for
              your team.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
