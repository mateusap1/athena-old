import React from 'react';

import Sidebar from '../components/Sidebar/Sidebar';
import Topbar from '../components/Topbar/Topbar';
import AddTransaction from '../components/AddTransaction/AddTransaction';
import AddReceivers from '../components/AddReceivers/AddReceivers';
import { useTransactions } from '../contexts/TransactionsContext';

import styles from './sendVerdict.module.scss';


export default function SendVerdict() {
  const { 
    getSentence,
    changeSentence,
    getDescription,
    changeDescription
  } = useTransactions();

  return (
    <>
      <Sidebar index={1} node_address={"192.168.0.1:5555"} />
      <Topbar index={3} />

      <div className={styles.mainContent}>
        <form>
          <AddTransaction 
            label="Accusation:" 
            buttonText="Select Accusation" 
            index="verdictAccusation" 
          />
          <br />
          <div className={styles.transactionParams}>
            <label htmlFor="sentence">Sentence:</label>
            <textarea 
              name="sentence"
              placeholder= {"Is the accused guilty or innocent? " +
                "If guilty, what is his sentence?"}
              cols="50" 
              rows="3"
              defaultValue={getSentence()}
              onChange={e => {
                changeSentence(e.target.value);
              }}
            />
          </div>
          <br />
          <div className={styles.transactionParams}>
            <label htmlFor="description">Description:</label>
            <textarea 
              name="description"
              placeholder="Describe why you made this decision"
              cols="50" 
              rows="3"
              defaultValue={getDescription()}
              onChange={e => {
                changeDescription(e.target.value);
              }}
            />
          </div>
          <br />
          <AddReceivers receiverIndex='verdict' />
        </form>
      </div>
    </>
  )
}