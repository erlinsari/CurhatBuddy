import { createBrowserRouter } from "react-router";
import Splash from "./components/Splash";
import Onboarding from "./components/Onboarding";
import Home from "./components/Home";
import Chat from "./components/Chat";
import Insight from "./components/Insight";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Splash,
  },
  {
    path: "/onboarding",
    Component: Onboarding,
  },
  {
    path: "/home",
    Component: Home,
  },
  {
    path: "/chat",
    Component: Chat,
  },
  {
    path: "/insight",
    Component: Insight,
  },
]);
