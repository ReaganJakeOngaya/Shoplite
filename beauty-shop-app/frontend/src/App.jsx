import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Products from "./pages/Products";
import { ThemeProvider } from "./context/ThemeContext";

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="flex h-screen">
          <Sidebar />
          <main className="flex-1 flex flex-col">
            <Navbar />
            <div className="p-4 flex-1 overflow-auto">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/products" element={<Products />} />
                {/* Add more routes here */}
              </Routes>
            </div>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;

