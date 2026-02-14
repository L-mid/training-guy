// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Training Guy',
  tagline: 'Quests to get stronger',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://training-guy.netlify.app',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'L-mid', // Usually your GitHub org/user name.
  projectName: 'training-guy', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],
  themeConfig: ({
    // ...
    navbar: {
      items: [
        { to: '/', label: 'Choices', position: 'left' },
        { to: '/curriculum/', label: 'Training 🦾', position: 'left' },
        { to: '/neetcode/', label: 'Solving game', position: 'left' },
        { to: '/make-a-game/', label: 'Make a game', position: 'left' },
        { to: '/gambling/', label: 'gambling', position: 'left' },
        { href: 'https://github.com/L-mid/training-guy', label: 'GitHub', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Play',
          items: [
            { label: 'Training 🦾', to: '/curriculum/' },
            { label: 'Solving game', to: '/neetcode/' },
            { label: 'Make a game', to: '/make-a-game/' },
            { label: 'gambling', to: '/gambling/' },
          ],
        },
        {
          title: 'More',
          items: [{ label: 'GitHub', href: 'https://github.com/L-mid/training-guy' }],
        },
      ],
      copyright: `© ${new Date().getFullYear()}`,
    },
  }),
};

export default config;