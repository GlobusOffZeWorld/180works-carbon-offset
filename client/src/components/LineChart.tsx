import React, { FC } from 'react';
import { Line } from 'react-chartjs-2';
import GraphData from '../models/GraphData'
import { Chart as ChartJS, registerables } from 'chart.js';


ChartJS.register(...registerables);


const LineChart: FC<GraphData<'line'>> = ({ data, options }: GraphData<'line'>) => {
    return <Line data={data} options={options} />;
}

export default LineChart;