
import React, { useState } from 'react';
import './styles.css'

const Table = () => {

  const [data, setData] = useState([
    { country: 'South Africa', count: 250},
    { country: 'Nigeria', count: 300},
    { country: 'Algeria', count: 358},
    { country: 'South Africa', count: 250},
    { country: 'Nigeria', count: 300},
  ]);

  return (
    <table>
      <thead>
        <tr>
          <th>Country</th>
          <th>Furnace count</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            <td>{row.country}</td>
            <td>{row.count}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default Table;