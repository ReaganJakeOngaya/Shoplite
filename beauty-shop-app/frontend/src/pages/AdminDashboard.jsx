import { useEffect, useState } from "react";

export default function AdminDashboard() {
  const [products, setProducts] = useState([]);
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");

  const fetchProducts = async () => {
    const res = await fetch("http://127.0.0.1:5000/api/products");
    const data = await res.json();
    setProducts(data);
  };

  const addProduct = async () => {
    const res = await fetch("http://127.0.0.1:5000/api/products", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, price }),
    });
    if (res.ok) {
      setName("");
      setPrice("");
      fetchProducts();
    }
  };

  const deleteProduct = async (id) => {
    await fetch(`http://127.0.0.1:5000/api/products/${id}`, {
      method: "DELETE",
    });
    fetchProducts();
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center text-rose-700">Admin Dashboard</h1>

      <div className="bg-white p-6 rounded-xl shadow-lg mb-10">
        <h2 className="text-xl font-semibold mb-4">Add Product</h2>
        <div className="flex gap-4 mb-4">
          <input
            type="text"
            placeholder="Product Name"
            className="flex-1 px-4 py-2 border rounded-md"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            type="number"
            placeholder="Price"
            className="w-32 px-4 py-2 border rounded-md"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
          />
        </div>
        <button
          className="bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded-xl"
          onClick={addProduct}
        >
          Add Product
        </button>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h2 className="text-xl font-semibold mb-4">Product List</h2>
        {products.length === 0 ? (
          <p>No products yet.</p>
        ) : (
          <ul className="space-y-3">
            {products.map((product) => (
              <li
                key={product.id}
                className="flex justify-between items-center bg-gray-100 px-4 py-2 rounded-md"
              >
                <div>
                  <p className="font-medium">{product.name}</p>
                  <p className="text-sm text-gray-600">${product.price}</p>
                </div>
                <button
                  onClick={() => deleteProduct(product.id)}
                  className="text-sm text-white bg-red-500 hover:bg-red-600 px-3 py-1 rounded-md"
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
