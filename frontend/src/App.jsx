import { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import { isLoggedIn } from "./api/auth";

function App() {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={<Login onLogin={() => setLoggedIn(true)} />}
        />
        <Route
          path="/signup"
          element={<Signup onLogin={() => setLoggedIn(true)} />}
        />
        <Route
          path="/dashboard"
          element={loggedIn ? <Dashboard onLogout={() => setLoggedIn(false)} /> : <Navigate to="/login" />}
        />
        <Route
          path="*"
          element={<Navigate to={loggedIn ? "/dashboard" : "/login"} />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;