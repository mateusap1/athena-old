import React from 'react';

import Sidebar from '../components/Sidebar/Sidebar';
import Topbar from '../components/Topbar/Topbar';
import AddTransaction from '../components/AddTransaction/AddTransaction';
import AddReceivers from '../components/AddReceivers/AddReceivers';
import styles from './sendAppeal.module.scss';


export default function SendAppeal() {
  return (
    <>
      <Sidebar index={1} node_address={"192.168.0.1:5555"} />
      <Topbar index={4} />

      <div className={styles.mainContent}>
        <form>
          <AddTransaction 
            label="Verdict:" 
            buttonText="Select Verdict" 
            index="appealVerdict" 
          />
          <br />
          <AddReceivers receiverIndex='appeal' />
        </form>
      </div>
    </>
  )
}