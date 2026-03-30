import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Cadastro from "./pages/Cadastro";
import Chat from "./pages/Chat";
import BaseDeConhecimento from "./pages/BaseDeConhecimento";
import RotaPrivada from "./components/RotaPrivada";
import RotaAdmin from "./components/RotaAdmin";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route
          path="/admin"
          element={
            <RotaPrivada>
              <Chat />
            </RotaPrivada>
          }
        />
        <Route
          path="/admin/base-de-conhecimento"
          element={
            <RotaAdmin>
              <BaseDeConhecimento />
            </RotaAdmin>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
