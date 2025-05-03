import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
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
  },
  {
    title: 'Comprehensive Blogs',
    Svg: require('@site/static/img/undraw_blog.svg').default,
    description: (
      <>
        Stay updated with the latest Kubernetes trends, tips, and best practices through our regularly updated blogs.
      </>
    ),
  },
  {
    title: 'Kubernetes Tools & Commands',
    Svg: require('@site/static/img/undraw_tools.svg').default,
    description: (
      <>
        Explore essential Kubernetes tools and commands to simplify your workflow and manage your clusters effectively.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
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
