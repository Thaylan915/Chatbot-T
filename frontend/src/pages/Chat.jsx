import Sidebar from "../components/Sidebar";
import ChatArea from "../components/ChatArea";
import "./Chat.css";

export default function Chat() {
  const perfil = localStorage.getItem("perfil") || "usuario";

  return (
    <div className="layout">
      <Sidebar tipo={perfil} />
      <ChatArea />
    </div>
  );
}
