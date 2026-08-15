import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import { UserProvider } from "./components/UserContext";

export const metadata: Metadata = { title: "DevFlow — Engineering Intelligence Platform", description: "Engineering intelligence workspace" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body><UserProvider><div className="app-shell"><Sidebar/><div className="main"><Topbar/><main className="content">{children}</main></div></div></UserProvider></body></html>;
}
