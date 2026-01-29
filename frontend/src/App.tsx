import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthContext, useAuthState } from "./hooks/useAuth";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Collection from "./pages/Collection";
import AddBottle from "./pages/AddBottle";
import BottleDetail from "./pages/BottleDetail";
import EditBottle from "./pages/EditBottle";
import Wishlist from "./pages/Wishlist";
import Distilleries from "./pages/Distilleries";
import DistilleryDetail from "./pages/DistilleryDetail";

export default function App() {
  const auth = useAuthState();

  return (
    <AuthContext.Provider value={auth}>
      <Layout>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/collection" element={<ProtectedRoute><Collection /></ProtectedRoute>} />
          <Route path="/bottles/add" element={<ProtectedRoute><AddBottle /></ProtectedRoute>} />
          <Route path="/bottles/:id" element={<ProtectedRoute><BottleDetail /></ProtectedRoute>} />
          <Route path="/bottles/:id/edit" element={<ProtectedRoute><EditBottle /></ProtectedRoute>} />
          <Route path="/wishlist" element={<ProtectedRoute><Wishlist /></ProtectedRoute>} />
          <Route path="/distilleries" element={<Distilleries />} />
          <Route path="/distilleries/:slug" element={<DistilleryDetail />} />
          <Route path="/" element={<Navigate to={auth.isLoggedIn ? "/collection" : "/login"} replace />} />
        </Routes>
      </Layout>
    </AuthContext.Provider>
  );
}
