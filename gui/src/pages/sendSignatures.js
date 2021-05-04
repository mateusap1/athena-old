import React from 'react';

import Sidebar from '../components/Sidebar/Sidebar';
import Topbar from '../components/Topbar/Topbar';
import AddTransaction from '../components/AddTransaction/AddTransaction';
import AddReceivers from '../components/AddReceivers/AddReceivers';
import styles from './sendSignatures.module.scss';


export default function SendSignatures() {
  return (
    <>
      <Sidebar index={1} node_address={"192.168.0.1:5555"} />
      <Topbar index={1} />

      <div className={styles.mainContent}>
        <form>
          <AddTransaction 
            label="Contract:" 
            buttonText="Select Contract" 
            index="signatureContract" 
          />
          <br />
          <AddReceivers receiverIndex='signature' />
        </form>
      </div>
    </>
  )
}