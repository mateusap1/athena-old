import React from 'react';

import Sidebar from '../components/Sidebar/Sidebar';

import styles from './notifications.module.scss';


export default function Notifications() {
  return (
    <>
      <Sidebar index={0} node_address={"192.168.0.1:5555"} />
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
              <td><button className={styles.saveButton}>Save</button></td>
            </tr>
            <tr>
              <td>
                <span>Martin Luther</span>
                <br />
                <span>55f889c738888077cea744994fc7802a</span>
              </td>
              <td>
                <span>May 6, 2021</span>
                <br />
                <span>08:22 PM</span>
              </td>
              <td>
                <span>Verdict</span>
              </td>
              <td>
                <span>May 8, 2021</span>
                <br />
                <span>08:22 PM</span>
              </td>
              <td><button className={styles.saveButton}>Save</button></td>
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
              <td><button className={styles.deleteButton}>Delete</button></td>
            </tr>
          </tbody>
        </table> 
      </div>
    </>
  )
}