import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        surface: {
          950: "#08111f",
          900: "#0d1728",
          850: "#111d31",
          800: "#162238",
        },
        accent: {
          cyan: "#22d3ee",
          emerald: "#34d399",
          amber: "#f59e0b",
        },
      },
      boxShadow: {
        panel: "0 18px 45px rgba(0, 0, 0, 0.28)",
      },
    },
  },
  plugins: [],
} satisfies Config;
