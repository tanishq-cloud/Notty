# Vite React TypeScript Application

A React application built with Vite, TypeScript, shadcn/ui, Zustand for state management, and react-i18next for internationalization. The application displays data in tables and charts using API data.

## Features

- ⚡️ Built with Vite for lightning-fast development
- 🎯 TypeScript for type safety
- 🎨 shadcn/ui for beautiful, accessible components
- 📊 Data visualization with tables and charts
- 🌐 Internationalization support (English, French, Spanish)
- 🔄 State management with Zustand
- 📱 Fully responsive design

## Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tanishq-cloud/Hoo.git
cd Hoo
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

## State Management

The application uses Zustand for state management. Store configurations can be found in `src/store/`:


## Internationalization

Languages are managed using react-i18next. Translation files are located in `public/locales/`:

- English: `en.json`
- French: `fr.json`
- Spanish: `es.json`

To switch languages:

```typescript
import { useTranslation } from 'react-i18next';

function Component() {
  const { i18n } = useTranslation();
  
  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };
}
```

## API Integration

The application integrates with two main endpoints:

1. Table Data:
   - Endpoint: `GET /posts?_page=1&_limit=10`
   - Used for paginated table display

2. Graph Data:
   - Endpoint: `GET /users`
   - Used for chart visualization

## Available Scripts

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

```

## Adding New Components

1. Install shadcn/ui components:
```bash
npx shadcn-ui@latest add [component-name]
```

2. Import and use in your components:
```typescript
import { Button } from "@/components/ui/button"
```


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Vite](https://vitejs.dev/)
- [React](https://reactjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Zustand](https://zustand-demo.pmnd.rs/)
- [react-i18next](https://react.i18next.com/)