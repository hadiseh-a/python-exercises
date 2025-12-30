import "bootstrap/dist/css/bootstrap.min.css";
import "./globals.css";
import Navbar from "@/components/Navbar";
import { DataProvider } from "@/context/DataContext";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-light">
        <DataProvider>
          <Navbar />
          <main className="container pt-5 mt-4"> {/* pt-5: padding-top کافی برای Navbar */}
            {children}
          </main>
        </DataProvider>
      </body>
    </html>
  );
}
