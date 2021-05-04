import React from 'react';

import Sidebar from '../components/Sidebar/Sidebar';

import styles from './settings.module.scss';


export default function Settings() {
  return (
    <>
      <Sidebar index={4} node_address={"192.168.0.1:5555"} />
      <div className={styles.mainContent}>
        <form>
          <div className={styles.nodeInfo}>
            <label htmlFor="node-address">Node:</label>
            <input type="text" name="node-address" placeholder="Address" />
            <input type="text" name="node-port" placeholder="Port" />
          </div>
          <br />
          <div className={styles.buttonContainer}>
            <button type="button">Save changes</button>
          </div>
        </form>
      </div>
    </>
  )
}