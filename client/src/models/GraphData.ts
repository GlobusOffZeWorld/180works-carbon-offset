import Chart, { Chart as ChartJS, registerables } from 'chart.js';




interface GraphData<T extends 'line' | 'bar'> {
    data: Chart.ChartData<T>;
    type?: Chart.ChartType;
    options?: Chart.ChartOptions<T>;
}

export default GraphData