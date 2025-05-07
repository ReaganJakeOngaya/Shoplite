import { useState } from "react";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const response = await fetch("http://127.0.0.1:5000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (data.token) {
      localStorage.setItem("token", data.token);
      alert("Logged in!");
      // redirect to dashboard
    } else {
      alert(data.error || "Login failed");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-tr from-pink-100 via-rose-50 to-purple-100 flex justify-center items-center">
      <div className="bg-white p-10 rounded-2xl shadow-xl w-full max-w-sm">
        <h2 className="text-2xl font-bold text-center text-rose-600 mb-6">Welcome Back</h2>
        <input
          type="text"
          placeholder="Username"
          className="w-full mb-4 px-4 py-2 border rounded-md"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full mb-6 px-4 py-2 border rounded-md"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          className="w-full bg-rose-500 hover:bg-rose-600 text-white py-2 rounded-xl transition"
          onClick={handleLogin}
        >
          Login
        </button>
      </div>
    </div>
  );
}

