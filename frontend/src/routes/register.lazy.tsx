import { createLazyFileRoute } from '@tanstack/react-router'
import RegisterPage from '@/pages/register-page/register-page'

export const Route = createLazyFileRoute('/register')({
  component: RegisterPage,
})



