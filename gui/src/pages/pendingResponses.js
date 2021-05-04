import React from 'react';
import { Link } from 'react-router-dom';

import Sidebar from '../components/Sidebar/Sidebar';

import styles from './pendingResponses.module.scss';


export default function PendingResponses() {
  return (
    <>
      <Sidebar index={3} node_address={"192.168.0.1:5555"} />
      <div className={styles.mainContent}>
        <table>
          <thead>
            <tr>
              <th>Sender</th>
              <th>Date</th>
              <th>Type</th>
              <th>Expire</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <span>John Calvin</span>
                <br />
                <span>
                  d355d063054082de487616fb582cf68b
                </span>
              </td>
              <td>
                <span>May 7, 2021</span>
                <br />
                <span>10:49 PM</span>
              </td>
              <td>
                <span>Contract</span>
              </td>
              <td>
                <span>May 9, 2021</span>
                <br />
                <span>10:49 PM</span>
              </td>
              <td>
                <Link to="/send-transaction/signature">
                  <button>Respond</button>
                </Link>
              </td>
            </tr>
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
              <td>
                <span>May 9, 2021</span>
                <br />
                <span>09:17 AM</span>
              </td>
              <td>
                <Link to="/send-transaction/verdict">
                  <button>Respond</button>
                </Link>
              </td>
            </tr>
          </tbody>
        </table> 
      </div>
    </>
  )
}