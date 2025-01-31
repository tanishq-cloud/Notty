import { createLazyFileRoute } from '@tanstack/react-router'
import Updates from '@/pages/Updates'
export const Route = createLazyFileRoute('/')({
  component: Updates
})

