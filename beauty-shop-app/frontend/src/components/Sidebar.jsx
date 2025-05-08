import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <aside className="w-64 bg-gray-100 dark:bg-gray-900 h-screen p-4">
      <nav className="flex flex-col space-y-4">
        <Link to="/" className="hover:underline">Dashboard</Link>
        <Link to="/products" className="hover:underline">Products</Link>
        <Link to="/services" className="hover:underline">Services</Link>
        <Link to="/orders" className="hover:underline">Orders</Link>
        <Link to="/bookings" className="hover:underline">Bookings</Link>
        <Link to="/analytics" className="hover:underline">Analytics</Link>
      </nav>
    </aside>
  );
};

export default Sidebar;
