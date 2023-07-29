import React, { FC } from 'react';
import { Bar } from 'react-chartjs-2';
import GraphData from '../models/GraphData'
import { Chart as ChartJS, registerables } from 'chart.js';

ChartJS.register(...registerables);



const BarChart: FC<GraphData<'bar'>> = ({ data, options }: GraphData<'bar'>) => {
    return <Bar data={data} options={options} />;
}

export default BarChart;