import React from 'react';
import { useTransactions } from '../../contexts/TransactionsContext';

import styles from './styles.module.scss';

export default function AddJudges() {
  const { 
    getJudgesID, 
    addJudgeId 
  } = useTransactions();
  
  let addJudgeRef = React.createRef();

  return (
    <div className={styles.transactionParams}>
      <label htmlFor="judges">Judges:</label>
      <div className={styles.judges}>
        {getJudgesID().map((fileElement, index) => {
          return (
            <div key={`judgeFileElement-${index}`}>
              <span>{index+1}: {fileElement.name}</span>
              <br />
            </div>
          );
        })}
      </div>
      <br />
      <button 
        name="judges" 
        onClick={() => {
          addJudgeRef.current.click();
        }}>Add Judge ID</button>
      <input 
        type="file" 
        style={{display: 'none'}}
        accept=".json"
        ref={addJudgeRef} 
        onChange={ (e) => {
          addJudgeId(Array.from(e.target.files).map(el => {
            return {
              name: el.name,
              path: el.path,
              type: el.type,
              size: el.size
            }
          }));
          e.target.value = null;
        }}
      />
    </div>
  );
}