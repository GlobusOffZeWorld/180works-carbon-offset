import React, { FC } from 'react';
import { Line } from 'react-chartjs-2';
import Chart, {Chart as ChartJS, LineElement, PointElement, LinearScale, Title, registerables } from 'chart.js';

ChartJS.register(...registerables);

interface GraphProps {
  data: Chart.ChartData<'line'>;
  type?: Chart.ChartType;
  options?: Chart.ChartOptions<'line'>;
}


const Graph:FC<GraphProps> = ({ data, options }: GraphProps) => {
  return <Line data={data} options={options} />;
}

export default Graph;