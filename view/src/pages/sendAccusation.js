import React from 'react';

import Sidebar from '../components/Sidebar/Sidebar';
import Topbar from '../components/Topbar/Topbar';
import AddTransaction from '../components/AddTransaction/AddTransaction';
import AddReceivers from '../components/AddReceivers/AddReceivers';
import styles from './sendAccusation.module.scss';


export default function SendAccusation() {
  return (
    <>
      <Sidebar index={1} node_address={"192.168.0.1:5555"} />
      <Topbar index={2} />

      <div className={styles.mainContent}>
        <form>
          <AddTransaction 
            label="Contract:" 
            buttonText="Select Contract" 
            index="accusationContract" 
          />
          <br />
          <AddTransaction 
            label="Accused:" 
            buttonText="Select Accused ID" 
            index="accusedID" 
          />
          <br />
          <AddReceivers receiverIndex='accusation' />
        </form>
      </div>
    </>
  )
}