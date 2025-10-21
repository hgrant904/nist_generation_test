# NIST Reports Frontend

Next.js-based frontend application for NIST security report automation.

## Technology Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Package Manager**: npm
- **Styling**: CSS (extensible to Tailwind CSS or other libraries)

## Development Setup

### Local Development (without Docker)

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp ../.env.example .env.local
# Edit .env.local with your configuration
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Building for Production

```bash
npm run build
npm start
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier
- `npm run type-check` - Run TypeScript type checking

## Project Structure

```
frontend/
├── src/
│   └── app/
│       ├── layout.tsx     # Root layout
│       ├── page.tsx       # Home page
│       ├── api/           # API routes (optional)
│       └── components/    # React components
├── public/                # Static assets
├── Dockerfile            # Production Dockerfile
├── Dockerfile.dev        # Development Dockerfile
├── next.config.js        # Next.js configuration
├── tsconfig.json         # TypeScript configuration
└── package.json
```

## Environment Variables

Create a `.env.local` file in the frontend directory with:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```
