import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const { isLoggedIn, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div style={{ minHeight: "100vh" }}>
      <header
        style={{
          background: "var(--color-primary)",
          color: "white",
          padding: "0.75rem 0",
          boxShadow: "var(--shadow)",
        }}
      >
        <nav className="container" style={{ display: "flex", alignItems: "center", gap: "1.5rem" }}>
          <Link to="/" style={{ color: "white", fontWeight: 700, fontSize: "1.25rem" }}>
            Whisky Tracker
          </Link>
          {isLoggedIn && (
            <>
              <Link to="/collection" style={{ color: "white" }}>Collection</Link>
              <Link to="/bottles/add" style={{ color: "white" }}>Add Bottle</Link>
              <Link to="/wishlist" style={{ color: "white" }}>Wishlist</Link>
              <Link to="/distilleries" style={{ color: "white" }}>Distilleries</Link>
              <div style={{ marginLeft: "auto" }}>
                <button
                  onClick={handleLogout}
                  style={{
                    background: "transparent",
                    color: "white",
                    border: "1px solid rgba(255,255,255,0.5)",
                    padding: "0.25rem 0.75rem",
                    borderRadius: "var(--radius)",
                  }}
                >
                  Logout
                </button>
              </div>
            </>
          )}
          {!isLoggedIn && (
            <div style={{ marginLeft: "auto", display: "flex", gap: "1rem" }}>
              <Link to="/login" style={{ color: "white" }}>Login</Link>
              <Link to="/register" style={{ color: "white" }}>Register</Link>
            </div>
          )}
        </nav>
      </header>
      <main className="container" style={{ padding: "2rem 1rem" }}>
        {children}
      </main>
    </div>
  );
}
