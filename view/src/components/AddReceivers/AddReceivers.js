import React from 'react';
import { useTransactions } from '../../contexts/TransactionsContext';

import styles from './styles.module.scss';

export default function AddReceivers({ receiverIndex }) {
  const { 
    getReceiversID, 
    addReceiverId 
  } = useTransactions();
  
  let addReceiverRef = React.createRef();

  return (
    <div className={styles.transactionParams}>
      <label htmlFor="receivers">Receivers:</label>
      <div className={styles.receivers}>
        {getReceiversID(receiverIndex).map((fileElement, index) => {
          return (
            <div key={`receiverFileElement-${index}`}>
              <span>{index+1}: {fileElement.name}</span>
              <br />
            </div>
          );
        })}
      </div>
      <br />
      <button 
        name="receivers" 
        onClick={() => {
          addReceiverRef.current.click();
        }}>Add Receiver ID</button>
      <input 
        type="file" 
        style={{display: 'none'}}
        accept=".json"
        ref={addReceiverRef} 
        onChange={ (e) => {
          addReceiverId(Array.from(e.target.files).map(el => {
            return {
              name: el.name,
              path: el.path,
              type: el.type,
              size: el.size
            }
          }), receiverIndex);
          e.target.value = null;
        }}
      />
    </div>
  );
}