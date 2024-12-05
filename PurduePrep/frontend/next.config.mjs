/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:5000/api/:path*', // http://127.0.0.1:5000/api/:path* for local. Hopefully just /api/:path* 'https://purdueprep-image-824914791442.us-central1.run.app/'
      },
    ];
  },
};

export default nextConfig;
