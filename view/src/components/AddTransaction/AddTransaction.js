import React from 'react';
import { useTransactions } from '../../contexts/TransactionsContext';

import styles from './styles.module.scss';

export default function AddTransaction({ label, buttonText, index }) {
  const { 
    getTransaction, 
    changeTransaction 
  } = useTransactions();
  
  let addTransactionRef = React.createRef();

  return (
    <div className={styles.transactionParams}>
      <label htmlFor="transaction">{label}</label>
      {getTransaction(index) ? (
        <span>{getTransaction(index).name}</span>
      ) : (
        <></>
      )}
      <br />
      <button 
        name="transaction" 
        onClick={() => {
          addTransactionRef.current.click();
        }}>{ buttonText }</button>
      <input 
        type="file" 
        style={{display: 'none'}}
        accept=".json"
        ref={addTransactionRef} 
        onChange={(e) => {
          changeTransaction({
            name: e.target.files[0].name,
            path: e.target.files[0].path,
            type: e.target.files[0].type,
            size: e.target.files[0].size
          }, index)
          e.target.value = null;
        }}
      />
    </div>
  );
}