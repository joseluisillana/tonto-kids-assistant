import { useEffect, useState } from "react";
import { useConversation } from "../features/conversation/useConversation.js";
import { AdminPage } from "../pages/AdminPage.js";
import { TontoPage } from "../pages/TontoPage.js";
import type { AppRoute } from "./routes.js";
import { getPathnameForRoute, getRouteFromPathname } from "./routes.js";

export function App() {
  const conversation = useConversation();
  const [route, setRoute] = useState<AppRoute>(() =>
    getRouteFromPathname(window.location.pathname),
  );

  useEffect(() => {
    function handlePopState() {
      setRoute(getRouteFromPathname(window.location.pathname));
    }

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  function navigate(nextRoute: AppRoute) {
    const pathname = getPathnameForRoute(nextRoute);
    window.history.pushState(null, "", pathname);
    setRoute(nextRoute);
  }

  return (
    <>
      <nav className="fixed left-1/2 top-4 z-50 flex -translate-x-1/2 gap-2 rounded-full border border-white/30 bg-slate-950/70 p-2 text-sm font-bold text-white shadow-xl backdrop-blur">
        <button
          className={`rounded-full px-4 py-2 ${
            route === "tonto" ? "bg-white text-slate-950" : "text-white/80"
          }`}
          onClick={() => navigate("tonto")}
          type="button"
        >
          Tonto
        </button>
        <button
          className={`rounded-full px-4 py-2 ${
            route === "admin" ? "bg-white text-slate-950" : "text-white/80"
          }`}
          onClick={() => navigate("admin")}
          type="button"
        >
          Admin
        </button>
      </nav>
      {route === "admin" ? (
        <AdminPage conversation={conversation} />
      ) : (
        <TontoPage conversation={conversation} />
      )}
    </>
  );
}
