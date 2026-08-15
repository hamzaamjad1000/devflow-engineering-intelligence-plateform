"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    const endpoint = isLogin ? "/login" : "/register";
    const payload = isLogin 
      ? { email, password }
      : { username, email, password };

    try {
      const res = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Authentication failed. Please try again.");
        setLoading(false);
        return;
      }

      if (isLogin) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "/dashboard";
      } else {
        setSuccess("Account created successfully! You can now log in.");
        setIsLogin(true); // Switch to login
        setUsername("");
        setPassword("");
      }
    } catch (err) {
      setError("Could not reach the server. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4 relative overflow-hidden">
      {/* Background visual accents */}
      <div className="absolute top-0 -left-4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 -right-4 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl" />

      <div className="w-full max-w-md relative z-10">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl shadow-slate-950/50">
          
          {/* Header */}
          <div className="text-center mb-8">
            <div className="w-12 h-12 rounded-xl bg-indigo-600 flex items-center justify-center font-bold text-white text-2xl mx-auto mb-4 shadow-lg shadow-indigo-500/20">
              D
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight">
              {isLogin ? "Welcome back" : "Create your account"}
            </h1>
            <p className="text-slate-400 text-sm mt-1.5">
              {isLogin ? "Log in to access your DevFlow workspace" : "Get started with your collaborative workspace"}
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">Username</label>
                <input
                  type="text"
                  placeholder="johndoe"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-lg text-white text-sm placeholder-slate-600 focus:outline-none focus:border-indigo-500 transition-all duration-200"
                  required={!isLogin}
                />
              </div>
            )}

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">Email address</label>
              <input
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-lg text-white text-sm placeholder-slate-600 focus:outline-none focus:border-indigo-500 transition-all duration-200"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-lg text-white text-sm placeholder-slate-600 focus:outline-none focus:border-indigo-500 transition-all duration-200"
                required
              />
            </div>

            {/* Notifications */}
            {error && (
              <p className="text-red-400 text-xs bg-red-500/10 border border-red-500/20 p-3 rounded-lg">
                {error}
              </p>
            )}
            {success && (
              <p className="text-emerald-400 text-xs bg-emerald-500/10 border border-emerald-500/20 p-3 rounded-lg">
                {success}
              </p>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-semibold transition-all duration-200 shadow-lg shadow-indigo-600/20 hover:shadow-indigo-500/30 disabled:opacity-50 cursor-pointer"
            >
              {loading ? "Please wait..." : isLogin ? "Sign In" : "Sign Up"}
            </button>
          </form>

          {/* Switch Link */}
          <div className="text-center mt-6 pt-6 border-t border-slate-800/60 text-sm">
            <span className="text-slate-500">
              {isLogin ? "New to DevFlow? " : "Already have an account? "}
            </span>
            <button
              type="button"
              onClick={() => {
                setIsLogin(!isLogin);
                setError("");
                setSuccess("");
              }}
              className="text-indigo-400 hover:text-indigo-300 font-semibold transition-all duration-200 cursor-pointer"
            >
              {isLogin ? "Create an account" : "Sign in instead"}
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}
