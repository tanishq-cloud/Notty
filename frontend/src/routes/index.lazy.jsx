import { createLazyFileRoute } from '@tanstack/react-router'
import LandingPage from '@/pages/landing'
export const Route = createLazyFileRoute('/')({
  component: LandingPage
})

