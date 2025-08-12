export const folders = [
  { id: "all", name: "All", icon: "folder" },
  { id: "ai", name: "Artificial intelligence", icon: "ai" },
  { id: "bio", name: "Biotechnologies", icon: "bio" },
  { id: "neuro", name: "Neuroscience", icon: "neuro" },
];

export const papersByFolder = {
  ai: [
    { id: "p1", title: "Sample Research Paper Title", authors: "John Doe, Jane Smith", year: 2024, journal: "Journal of Computer Science", type: "PDF" },
    { id: "p2", title: "Another Paper", authors: "Alice Dupond", year: 2023, journal: "Nature Neuroscience", type: "PDF" },
  ],
  bio: [],
  neuro: [],
  all: [{ id: "p1", title: "Sample Research Paper Title", authors: "John Doe, Jane Smith", year: 2024, journal: "Journal of Computer Science", type: "PDF" },
    { id: "p2", title: "Another Paper", authors: "Alice Dupond", year: 2023, journal: "Nature Neuroscience", type: "PDF" },
  ],
};
