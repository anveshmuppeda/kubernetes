import React from 'react';
import styles from './FixedAnnouncement.css';

export default function FixedAnnouncement() {
  return (
    <div className={styles.announcement}>
      📢 <b>XYZ Blog is out now!</b> Check it out <a href="/blog/xyz" target="_blank" rel="noopener noreferrer">here</a>.
    </div>
  );
}