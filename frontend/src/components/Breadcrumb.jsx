import Link from "next/link";
import HomeIcon from "@mui/icons-material/Home";
import NavigateNextIcon from "@mui/icons-material/NavigateNext";
import styles from "@/styles/Breadcrumb.module.css";

export default function Breadcrumb({ items = [] }) {
  let displayItems = items;

  if (items.length > 3) {
    displayItems = [
      { label: "...", href: null },
      items[items.length - 2],
      items[items.length - 1], 
    ];
  }

  return (
    <div className={styles.breadcrumb}>
      <Link href="/" className={styles.breadcrumbLink}>
        <HomeIcon style={{ fontSize: 35 }} />
      </Link>

      {displayItems.map((item, index) => (
        <span key={index} className={styles.breadcrumbItem}>
          <NavigateNextIcon
            className={styles.separator}
            style={{ fontSize: 25 }}
          />
          {item.href ? (
            <Link href={item.href} className={styles.breadcrumbLink}>
              {item.label}
            </Link>
          ) : (
            <span className={styles.breadcrumbText}>{item.label}</span>
          )}
        </span>
      ))}
    </div>
  );
}
