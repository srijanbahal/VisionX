import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { ThemeProvider, ThemeToggle } from '../components/ThemeProvider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'VisionX - Image Processing App',
  description: 'Advanced image processing application with multiple algorithms',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-background antialiased`}>
        <ThemeProvider>
          <header className="flex items-center justify-between py-6 px-4 border-b bg-background/80 sticky top-0 z-50">
            <div className="flex items-center gap-2">
              <span className="text-2xl font-bold tracking-tight text-primary">VisionX</span>
              <span className="text-sm text-muted-foreground ml-2">Interactive Computer Vision</span>
            </div>
            <ThemeToggle />
          </header>
          <main className="container mx-auto py-8 px-4">
            {children}
          </main>
        </ThemeProvider>
      </body>
    </html>
  )
}
