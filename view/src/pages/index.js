import React from 'react';
import ReactDOM from 'react-dom';
import { HashRouter, Route, Switch, Redirect } from 'react-router-dom';

import { TransactionsContextProvider } from '../contexts/TransactionsContext';
import Notifications from './notifications';
import MyTransactions from './myTransactions';
import PendingResponses from './pendingResponses';
import Settings from './settings';
import SendContracts from './sendContracts';
import SendSignatures from './sendSignatures';
import SendAccusation from './sendAccusation';
import SendVerdict from './sendVerdict';
import SendAppeal from './sendAppeal';

ReactDOM.render(
  <HashRouter>
    <Switch>
      <Route path="/notifications" exact component={ Notifications } />
      <Redirect from="/" exact to="/notifications" />
      <Route path="/send-transaction/contract">
        <TransactionsContextProvider>
          <SendContracts />
        </TransactionsContextProvider>
      </Route>
      <Route path="/send-transaction/signature">
        <TransactionsContextProvider>
          <SendSignatures />
        </TransactionsContextProvider>
      </Route>
      <Route path="/send-transaction/accusation">
        <TransactionsContextProvider>
          <SendAccusation />
        </TransactionsContextProvider>
      </Route>
      <Route path="/send-transaction/verdict">
        <TransactionsContextProvider>
          <SendVerdict />
        </TransactionsContextProvider>
      </Route>
      <Route path="/send-transaction/appeal">
        <TransactionsContextProvider>
          <SendAppeal />
        </TransactionsContextProvider>
      </Route>
      <Redirect from="/send-transaction" exact to="/send-transaction/contract" />
      <Route path="/my-transactions" exact component={ MyTransactions } />
      <Route path="/pending-responses" exact component={ PendingResponses } />
      <Route path="/settings" exact component={ Settings } />
    </Switch>
  </HashRouter>, 
  document.getElementById("root")
)