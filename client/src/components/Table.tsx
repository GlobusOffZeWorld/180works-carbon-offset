
import React from 'react';
import './styles.css'

interface District {
    district: string,
    count: number
}

interface TableProps {
    districts: District[],
}

const Table = ({districts}: TableProps) => {

  return (
    <table>
      <thead>
        <tr>
          <th>Country</th>
          <th>Furnace count</th>
        </tr>
      </thead>
      <tbody>
        {districts.map((row, index) => (
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