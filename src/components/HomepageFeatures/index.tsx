import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
  link: string; // Add a link property
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Step-by-Step Tutorials',
    Svg: require('@site/static/img/undraw_tutorial.svg').default,
    description: (
      <>
        Learn Kubernetes with detailed, step-by-step tutorials designed for beginners and advanced users alike. Start mastering Kubernetes today!
      </>
    ),
    link: '/kubernetes/docs/intro', // Add a specific link
  },
  {
    title: 'Comprehensive Blogs',
    Svg: require('@site/static/img/undraw_blog.svg').default,
    description: (
      <>
        Stay updated with the latest Kubernetes trends, tips, and best practices through our regularly updated blogs.
      </>
    ),
    link: '/kubernetes/blog', // Add a specific link
  },
  {
    title: 'Kubernetes Tools & Commands',
    Svg: require('@site/static/img/undraw_tools.svg').default,
    description: (
      <>
        Explore essential Kubernetes tools and commands to simplify your workflow and manage your clusters effectively.
      </>
    ),
    link: '/kubernetes/commands/intro', // Add a specific link
  },
];

function Feature({ title, Svg, description, link }: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        {/* Use the link property for the hyperlink */}
        <a href={link}>
          <Svg className={styles.featureSvg} role="img" />
        </a>
      </div>
      <div className="text--center padding-horiz--md">
        <a href={link}>
          <Heading as="h3">{title}</Heading>
        </a>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
