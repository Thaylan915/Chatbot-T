import { Navigate } from "react-router-dom";

/**
 * Protege rotas que exigem autenticação (qualquer perfil).
 * Redireciona para "/" se não houver token no localStorage.
 */
export default function RotaPrivada({ children }) {
  const token = localStorage.getItem("access_token");
  if (!token) {
    return <Navigate to="/" replace />;
  }
  return children;
}
