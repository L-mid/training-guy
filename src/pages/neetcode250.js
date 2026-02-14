import React, { useEffect } from 'react';
import Layout from '@theme/Layout';

const TARGET = 'https://neetcode.io/practice/practice/neetcode250';

export default function Neetcode250Redirect() {
  useEffect(() => {
    // Client-side redirect to NeetCode 250.
    window.location.replace(TARGET);
  }, []);

  return (
    <Layout title="Redirecting…" description="Redirecting to NeetCode 250">
      <main style={{ padding: '2rem 1rem', maxWidth: 720, margin: '0 auto' }}>
        <h1>Redirecting…</h1>
        <p>
          Taking you to NeetCode 250. If nothing happens, click{' '}
          <a href={TARGET}>this link</a>.
        </p>
      </main>
    </Layout>
  );
}
