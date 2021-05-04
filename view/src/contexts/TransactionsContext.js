import React, { createContext, useState, ReactNode, useContext } from 'react';

export const TransactionsContext = createContext({});

export function TransactionsContextProvider({ children }) {
  const [storedRules, setStoredRules] = useState([""]);
  const [storedSentence, setStoredSentence] = useState("");
  const [storedDescription, setStoredDescription] = useState("");
  const [judgeIDs, setJudgeIDs] = useState([]);
  const [receiversID, setReceiversID] = useState({
    contract: [],
    signature: [],
    accusation: [],
    verdict: [],
    appeal: []
  });
  const [storedTransaction, setStoredTransaction] = useState({});

  function getTransaction(index) {
    const storedTransaction = JSON.parse(localStorage.getItem('storedTransaction'));
    if (storedTransaction == undefined || !(index in storedTransaction)){
      return null;
    }
    else {
      return storedTransaction[index];
    }
  }

  function changeTransaction(file, index) {
    let updatedTransaction = JSON.parse(localStorage.getItem('storedTransaction'));
    if (updatedTransaction == null) {
      localStorage.setItem('storedTransaction', JSON.stringify(storedTransaction));
      updatedTransaction = JSON.parse(localStorage.getItem('storedTransaction'));
    }

    updatedTransaction[index] = file;

    setStoredTransaction(updatedTransaction);
    localStorage.setItem('storedTransaction', JSON.stringify(updatedTransaction));
  }

  function changeRules(newRules) {
    setStoredRules(newRules);
    localStorage.setItem('storedRules', JSON.stringify(newRules));
  }

  function addRule() {
    changeRules([...getRules(), ""]);
  };

  function getRules() {
    return JSON.parse(localStorage.getItem('storedRules')) || [""];
  }

  function changeSentence(newSentence) {
    setStoredSentence(newSentence);
    localStorage.setItem('storedSentence', JSON.stringify(newSentence));
  }

  function getSentence() {
    return JSON.parse(localStorage.getItem('storedSentence')) || "";
  }

  function changeDescription(newDescription) {
    setStoredDescription(newDescription);
    localStorage.setItem('storedDescription', JSON.stringify(newDescription));
  }

  function getDescription() {
    return JSON.parse(localStorage.getItem('storedDescription')) || "";
  }

  function changeJudges(newJudges) {
    setJudgeIDs(newJudges);
    localStorage.setItem('judgesID', JSON.stringify(newJudges));
  }

  function addJudgeId(files) {
    changeJudges([...getJudgesID(), ...Array.from(files)]);
  }

  function getJudgesID() {
    return JSON.parse(localStorage.getItem('judgesID')) || [];
  }

  function changeReceivers(newReceivers, index) {
    let updatedReceivers = JSON.parse(localStorage.getItem('receiversID'));
    if (updatedReceivers == null) {
      localStorage.setItem('receiversID', JSON.stringify(receiversID));
      updatedReceivers = JSON.parse(localStorage.getItem('receiversID'));
    }

    updatedReceivers[index] = newReceivers;

    setReceiversID(updatedReceivers);
    localStorage.setItem('receiversID', JSON.stringify(updatedReceivers));
  }

  function addReceiverId(files, index) {
    changeReceivers([...getReceiversID(index), ...Array.from(files)], index);
  }

  function getReceiversID(index) {
    const receivers = JSON.parse(localStorage.getItem('receiversID'));
    if (receivers == undefined || !(index in receivers)){
      return [];
    }
    else {
      return receivers[index];
    }
  }
 
  return (
    <TransactionsContext.Provider 
      value={{ 
        getRules,
        addRule,
        changeRules,
        getJudgesID,
        addJudgeId,
        changeJudges,
        getReceiversID,
        addReceiverId,
        changeReceivers,
        getTransaction,
        changeTransaction,
        getSentence,
        changeSentence,
        getDescription,
        changeDescription
      }}>
      {children}
    </TransactionsContext.Provider>
  )
}

export const useTransactions = () => {
  return useContext(TransactionsContext);
}