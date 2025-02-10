import { createLazyFileRoute } from "@tanstack/react-router";
import LandingPage from "@/pages/landing/landing";
export const Route = createLazyFileRoute("/")({
  component: LandingPage,
});
