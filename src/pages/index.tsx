import type { ReactNode } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Start Kubernetes Hands-On - 5min ⏱️
          </Link>
        </div>
        <div className={styles.buttons}>
          <Link
            className="button button--outline button--lg"
            to="/blog">
            Read Latest Blogs 📝
          </Link>
        </div>
        <div className={styles.hitCounter}>
          <p>Website Views:</p>
          <div id="sfcyskq12yb9xjpkmf7tqcssx1m7d1glsjj"></div>
          <script
            type="text/javascript"
            src="https://counter4.optistats.ovh/private/counter.js?c=yskq12yb9xjpkmf7tqcssx1m7d1glsjj&down=async"
            async
          ></script>
          <noscript>
            <a
              href="https://github.com/anveshmuppeda/kubernetes"
              title="Kubernetes HandsOn Guides">
              <img
                src="https://counter4.optistats.ovh/private/freecounterstat.php?c=yskq12yb9xjpkmf7tqcssx1m7d1glsjj"
                border="0"
                title="Kubernetes HandsOn Guides"
                alt="Kubernetes HandsOn Guides"
              />
            </a>
          </noscript>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Master Kubernetes with hands-on tutorials, blogs, and tools.">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
