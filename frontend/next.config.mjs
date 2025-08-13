/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  experimental: {
    turbo: false, // Explicitly disable Turbopack
  },
  // Aggressive hot reload settings for Docker
  webpack: (config, { dev }) => {
    if (dev) {
      config.watchOptions = {
        poll: 500,
        aggregateTimeout: 100,
        ignored: ['**/node_modules', '**/.git', '**/.next'],
      }
    }
    return config
  }
};

export default nextConfig;
