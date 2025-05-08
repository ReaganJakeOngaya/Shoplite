import { useContext } from "react";
import { ThemeContext } from "../context/ThemeContext";
import { Moon, Sun } from "lucide-react";

const Navbar = () => {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <nav className="flex justify-between items-center px-6 py-3 shadow bg-white dark:bg-gray-800">
      <h1 className="text-xl font-bold">Beauty Shop Admin</h1>
      <button
        onClick={toggleTheme}
        className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
      >
        {theme === "light" ? <Moon size={20} /> : <Sun size={20} />}
      </button>
    </nav>
  );
};

export default Navbar;
