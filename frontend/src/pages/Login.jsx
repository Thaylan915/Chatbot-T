import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import Header from "../components/Header";
import "./Styles.css";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setErro("");
    setCarregando(true);

    try {
      const resposta = await fetch("/api/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password: senha }),
      });

      const dados = await resposta.json();

      if (!resposta.ok) {
        setErro(dados.error || "Credenciais inválidas.");
        return;
      }

      localStorage.setItem("access_token", dados.access);
      localStorage.setItem("refresh_token", dados.refresh);
      localStorage.setItem("username", dados.username);
      localStorage.setItem("email", dados.email);
      localStorage.setItem("nome", dados.nome);
      localStorage.setItem("perfil", dados.perfil);

      navigate("/admin");
    } catch {
      setErro("Erro ao conectar com o servidor.");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="pagina">
      <Header />

      <div className="conteudo">
        <div className="card">
          <h2>Login</h2>

          <form onSubmit={handleSubmit}>
            <label>
              <span>Usuário</span>
              <input
                type="text"
                placeholder="Digite seu usuário ou e-mail"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </label>

            <label>
              <span>Senha</span>
              <input
                type="password"
                placeholder="Digite sua senha"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                required
              />
            </label>

            {erro && <p className="erro">{erro}</p>}

            <Link to="/cadastro">Cadastrar-se</Link>

            <button className="btnEntrar" type="submit" disabled={carregando}>
              {carregando ? "Entrando..." : "Entrar"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
