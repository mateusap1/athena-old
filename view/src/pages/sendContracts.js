import React from 'react';

import Sidebar from '../components/Sidebar/Sidebar';
import Topbar from '../components/Topbar/Topbar';
import AddJudges from '../components/AddJudges/AddJudges';
import AddReceivers from '../components/AddReceivers/AddReceivers';
import { useTransactions } from '../contexts/TransactionsContext';

import { IoIosAddCircle } from "react-icons/io";
import styles from './sendContracts.module.scss';


export default function SendContracts() {
  const { 
    getRules, 
    changeRules,
    addRule
  } = useTransactions();

  return (
    <>
      <Sidebar index={1} node_address={"192.168.0.1:5555"} />
      <Topbar index={0} />

      <div className={styles.mainContent}>
        <form>
          <div className={styles.transactionParams}>
            <label htmlFor="rule-0">Rules:</label>
            <div className={styles.rules}>
              {getRules().map((text, index) => {
                return (
                  <div key={`rule-${index}`}>
                    {index < (getRules().length - 1) ? (
                      <textarea 
                        name={`rule-${index}`} 
                        cols="50" 
                        rows="1"
                        defaultValue={text}
                        onChange={e => {
                          let updatedRules = [...getRules()];
                          updatedRules[index] = e.target.value;
                          changeRules(updatedRules);
                        }}
                      />
                    ) : (
                      <textarea 
                        name={`rule-${index}`} 
                        cols="50" 
                        rows="3"
                        defaultValue={text}
                        onChange={e => {
                          let updatedRules = [...getRules()];
                          updatedRules[index] = e.target.value;
                          changeRules(updatedRules);
                        }}
                      />
                    )}
                  <br />
                </div>
              );
            })}</div>

            <IoIosAddCircle 
              className={styles.addButton} 
              size="40px" 
              color="#40b64c" 
              onClick={() => {addRule()}}
            />
          </div>
          <br />
          <AddJudges />
          <br />
          <div className={styles.transactionParams}>
            <label htmlFor="expireDate">Expire:</label>
            <input type="date" id="expireDate" name="expireDate" /> 
          </div>
          <br />
          <AddReceivers receiverIndex='contract' />
        </form>
      </div>
    </>
  )
}