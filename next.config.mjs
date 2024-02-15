/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    RECEIVER_HOSTNAME: process.env.RECEIVER_HOSTNAME,
  },
};

export default nextConfig;
