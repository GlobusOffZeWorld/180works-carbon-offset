import React, { FC } from 'react';
import { Bar } from 'react-chartjs-2';
import Chart, { Chart as ChartJS, registerables } from 'chart.js';

ChartJS.register(...registerables);

interface GraphProps {
    data: Chart.ChartData<'bar'>;
    type?: Chart.ChartType;
    options?: Chart.ChartOptions<'bar'>;
}


const BarChart: FC<GraphProps> = ({ data, options }: GraphProps) => {
    return <Bar data={data} options={options} />;
}

export default BarChart;