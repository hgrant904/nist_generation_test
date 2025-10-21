export const metadata = {
  title: 'NIST Reports',
  description: 'Automate NIST security report generation',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
