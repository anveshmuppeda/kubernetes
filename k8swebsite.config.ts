import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const { version } = require('./package.json'); // Import version from package.json

const config: Config = {
  // Update the title and tagline
  title: 'Kubernetes Hands-On Guides',
  tagline: 'Master Kubernetes with step-by-step tutorials and blogs',
  favicon: 'img/logo.png',

  // Set the production url of your site here
  url: 'https://anveshmuppeda.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/kubernetes/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'anveshmuppeda', // Usually your GitHub org/user name.
  projectName: 'kubernetes', // Usually your repo name.
  deploymentBranch: 'main',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

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
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/anveshmuppeda/kubernetes/tree/dev/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/anveshmuppeda/kubernetes/tree/dev/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'commands', // Unique ID for the commands plugin
        path: 'commands', // Path to the commands directory
        routeBasePath: 'commands', // URL path for the commands section
        sidebarPath: require.resolve('./sidebars.js'), // Sidebar configuration for commands
        editUrl: 'https://github.com/anveshmuppeda/kubernetes/tree/dev/',
      },
    ],
    [
      require.resolve('docusaurus-lunr-search'),
      {
        languages: ['en', 'fr'], // English and French
        highlightResult: true, // Highlight search results
        maxHits: 10, // Show up to 10 results
      },
    ],
    [
      '@docusaurus/theme-live-codeblock', // Wrap this plugin in an array
      {},
    ],
  ],

  themeConfig: {
    liveCodeBlock: {
      /**
       * The position of the live playground, above or under the editor
       * Possible values: "top" | "bottom"
       */
      playgroundPosition: 'bottom',
    },
    announcementBar: {
      id: 'announcement', // Unique ID for the announcement
      content: 
        '🎉️ <b><a target="_blank" href="https://github.com/anveshmuppeda/kubernetes/releases/tag/${version}">Docusaurus v${version}</a> is out!</b> 🥳️',
      backgroundColor: '#fafbfc',
      textColor: '#091E42',
      isCloseable: false,
    },
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Kubernetes Guides', // Keep the title as is
      logo: {
        alt: 'Kubernetes Logo',
        src: 'img/logo.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Tutorial',
        },
        {
          position: 'left',
          label: 'Commands',
          to: '/commands/intro', // URL path for the commands section
        },
        { to: '/blog', label: 'Blog', position: 'left' },
        {
          href: 'https://github.com/anveshmuppeda/kubernetes',
          label: 'GitHub',
          position: 'right',
        },
        {
          type: 'search', // Add the search bar to the navbar
          position: 'right',
        },
        {
          type: 'html', // Use a custom component for the version number
          position: 'right', // Place it after the search bar
          value: `<a href="https://github.com/anveshmuppeda/kubernetes/releases/tag/${version}" target="_blank" rel="noopener noreferrer" class="navbar-version">Version ${version}</a>`, // Use a link with a custom class
        },
        
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Tutorial',
              to: '/docs/intro',
            },
            {
              label: 'Commands',
              to: '/commands/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Medium',
              href: 'https://medium.com/@muppedaanvesh',
            },
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/in/anveshmuppeda/',
            },
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/users/16485310/anvesh-muppeda',
            },
            {
              label: 'X',
              href: 'https://x.com/Anvesh66743877',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/anveshmuppeda',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Anvesh Muppeda.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
