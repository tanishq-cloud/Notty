import { createLazyFileRoute } from '@tanstack/react-router'
import Updates from '@/pages/landing'
export const Route = createLazyFileRoute('/')({
  component: Updates
})

