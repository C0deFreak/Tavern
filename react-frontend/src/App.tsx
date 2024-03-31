import React, { useEffect, useState } from 'react';
import Message from './Message';

function App() {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("http://localhost:2371/members")
      .then(res => res.json())
      .then(data => {
        setData(data);
        console.log(data);
      })
      
  }, []);


  return (
    <div>
      <div>
        {(typeof data.members === 'undefined') ? (
          <p>Loading...</p>
        ): (
          data.members.map((member, i) => (
            <p key={i}>{member}</p>
          ))
        )}
      </div>
      <div><Message /></div>
    </div>
  )
}

export default App;
