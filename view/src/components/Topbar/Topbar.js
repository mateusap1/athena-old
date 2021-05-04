import React from 'react';
import { Link } from 'react-router-dom';

import styles from './styles.module.scss';


export default function Topbar({ index }) {
  return (
      <div className={styles.mainContent}>
        <table>
          <thead>
            <tr>
              <th className={index == 0 ? styles.selected : ''}>
                <Link to="/send-transaction/contract">Contract</Link>
              </th>
              <th className={index == 1 ? styles.selected : ''}>
                <Link to="/send-transaction/signature">Signature</Link>
              </th>
              <th className={index == 2 ? styles.selected : ''}>
                <Link to="/send-transaction/accusation">Accusation</Link>
              </th>
              <th className={index == 3 ? styles.selected : ''}>
                <Link to="/send-transaction/verdict">Verdict</Link>
              </th>
              <th className={index == 4 ? styles.selected : ''}>
                <Link to="/send-transaction/appeal">Appeal</Link>
              </th>
            </tr>
          </thead>
        </table> 
      </div>
  );
}