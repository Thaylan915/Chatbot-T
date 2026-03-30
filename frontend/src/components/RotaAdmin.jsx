import { Navigate } from "react-router-dom";

/**
 * Protege rotas exclusivas do perfil admin.
 * Redireciona para "/admin" se o usuário estiver autenticado mas não for admin.
 * Redireciona para "/" se não houver token.
 */
export default function RotaAdmin({ children }) {
  const token = localStorage.getItem("access_token");
  const perfil = localStorage.getItem("perfil");

  if (!token) {
    return <Navigate to="/" replace />;
  }

  if (perfil !== "admin") {
    return <Navigate to="/admin" replace />;
  }

  return children;
}
