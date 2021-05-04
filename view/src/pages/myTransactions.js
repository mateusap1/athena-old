import React from 'react';

import Sidebar from '../components/Sidebar/Sidebar';

import styles from './myTransactions.module.scss';


export default function MyTransactions() {
  return (
    <>
      <Sidebar index={2} node_address={"192.168.0.1:5555"} />
      <div className={styles.mainContent}>
        <table>
          <thead>
            <tr>
              <th>Sender</th>
              <th>Date</th>
              <th>Type</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <span>John Knox</span>
                <br />
                <span>34820d37ed2a2f1236e1a8f31d875819</span>
              </td>
              <td>
                <span>May 6, 2021</span>
                <br />
                <span>09:17 AM</span>
              </td>
              <td>
                <span>Accusation</span>
              </td>
              <td><button>Browse</button></td>
            </tr>
          </tbody>
        </table> 
      </div>
    </>
  )
}