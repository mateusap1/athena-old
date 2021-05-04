import React from 'react';

import { Link } from 'react-router-dom';
import styles from './styles.module.scss';


export default function({ index, node_address }) {
  return (
    <div className={styles.sidebar}>
      <h1>Athena</h1>
      <div className={styles.activeContracts}>
        <span>Active contracts</span>
        <br />
        <span>02</span>
      </div>
      <div className={styles.currentTrials}>
        <span>Current trials</span>
        <br />
        <span>00</span>
      </div>
      <ul>
          <li className={index == 0 ? styles.selected : ''}>
            <Link to="/notifications">Notifications</Link>
          </li>
          <li className={index == 1 ? styles.selected : ''}>
            <Link to="/send-transaction">Send transaction</Link>
          </li>
          <li className={index == 2 ? styles.selected : ''}>
            <Link to="/my-transactions">My transactions</Link>
          </li>
          <li className={index == 3 ? styles.selected : ''}>
            <Link to="/pending-responses">Pending responses</Link>
          </li>
          <li className={index == 4 ? styles.selected : ''}>
            <Link to="/settings">Settings</Link>
          </li>
      </ul> 
      <div className={styles.node}>
          {node_address ? (
            <p><span className={styles.connected}>Connected</span> to {node_address}</p>
          ) : (
            <p><span className={styles.notConnected}>Not Connected</span></p>
          )}
      </div>
    </div>
  );
}