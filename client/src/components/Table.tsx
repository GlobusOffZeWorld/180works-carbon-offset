
import React, { useState } from 'react';
import './styles.css'

interface District {
    district: string,
    count: number
}

const Table = (districts: District[]) => {

  const [data, setData] = useState<District[]>([
    { district: 'South Africa', count: 250},
    { district: 'Nigeria', count: 300},
    { district: 'Algeria', count: 358},
    { district: 'South Africa', count: 250},
    { district: 'Nigeria', count: 300},
  ]);

  setData(districts)

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
            <td>{row.district}</td>
            <td>{row.count}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default Table;