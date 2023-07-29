import React, { FC, ReactElement, useState, useEffect, ReactNode } from 'react';
import LineChart from './components/LineChart';
import BarChart from './components/BarChart';
import Table from './components/Table';
import './App.css'
import axios from 'axios'
import Chart, { Chart as ChartJS } from 'chart.js';
import District from './models/District';


interface Details {
    stoves_num: number,
    date: string,
    work_num: number,
    work_time: number
}

interface GraphInfo {
    type: string,
    data: {
        labels: string[] | number[],
        datasets: [
            {
                label: string,
                data: number[],
                fill: boolean,
                borderColor: string,
                backgroundColor?: string
                tension: number
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: boolean
            }
        }
    }
}

const App: FC = () => {

    const [details, setDetails] = useState<Details[]>([])

    const [districts, setDistricts] = useState<District[]>([])

    districts.sort((a: District, b: District) => {
        return b.count - a.count
    })

    const getData = async () => {
        const { data } = await axios.get('http://127.0.0.1:8000/?format=json');
        setDetails(data);

    };
    const getDistricts = async () => {
        const { data } = await axios.get('http://127.0.0.1:8000/districts/?format=json');
        setDistricts(data)
    };

    const reversedDetails = [...details].reverse()

    const totalInfo = {
        stovesCount: 0,
        startCount: 0,
        hoursCount: 0,
    }

    totalInfo.stovesCount = districts.reduce<number>((acc: number, { count }: District) => {
        return acc + count
    }, 0)


    for (const info of reversedDetails) {
        totalInfo.startCount += info.work_num
        totalInfo.hoursCount += info.work_time
    }

    const days = [...Array(31).keys()].slice(1)

    const makeDiagram: (type: string, label: string, labels: string[] | number[], data: number[]) => GraphInfo = (type, label, labels, data)  => {
        return {
            type: type,
            data: {
                labels: labels,
                datasets: [
                    {
                        label: label,
                        data: data,
                        fill: false,
                        backgroundColor: 'rgba(89, 84, 86, 0.5)',
                        borderColor: 'rgb(89, 84, 86)',
                        tension: 0.1
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        }
    }

    const createChart = ({ type, data, options }: GraphInfo): ReactNode => {
        switch (type) {
            case 'line':
                return <LineChart data={data as Chart.ChartData<'line'>} options={options as Chart.ChartOptions<'line'>} />
            case 'bar':
                return <BarChart data={data as Chart.ChartData<'bar'>} options={options as Chart.ChartOptions<'bar'>} />

        }
    }

    useEffect(() => {
        getData();
        getDistricts();
    }, []);

    const slicedDistricts: District[] = districts.slice(0, 6)

    const diagrams = [
        makeDiagram('line', 'Amount of working stoves', days, reversedDetails.map((detail: Details) => detail.stoves_num)),
        makeDiagram('line', 'Average number of launches', days, reversedDetails.map((detail: Details) => detail.work_num)),
        makeDiagram('line', 'Working hours', days, reversedDetails.map((detail: Details) => detail.work_time)),
        makeDiagram('bar', 'Count of stoves in each district', districts.map((el) => el.district), districts.map((el) => el.count))
    ]

    const missionInfo: string = `Использование печек существенно снижает потребление древесины, а следовательно и выброс CO2 в атмосферу.
    180.works хочет получить дополнительное финансирование за счет участия в программе Carbon Credits - ценные бумаги, которые выдаются за снижение выбросов CO2.
    Но для этого необходимо знать реальное использование печек.
    Сейчас компания исследует возможность встраивания в печки термодатчиков передающих данные по LoRaWAN протоколу.`

    const mainSiteReference = <a href="https://180.works/#/carbon-offset">180.works</a>
    
    return (
        <div>
            <div className="header">
                <div className="header__background-image"></div>
                <div className="header__content">
                    <h1>Let's save Africa</h1>
                    <p>Некоммерческая организация {mainSiteReference} занимается восстановлением лесов в Африке. Частью этой программы является установка печек для приготовления пищи.

                    </p>
                    <p>{missionInfo}</p>
                </div>
            </div>

            <div className='diagrams-container'>
                {diagrams.map(({ type, data, options }: GraphInfo, index) => (
                    <div className="diagrams-container__chart" key={index}>
                        {createChart({ type, data, options })}
                    </div>
                ))}
            </div>

            <div className="region-table">
                <Table districts={slicedDistricts} />
            </div>
            <div className="about">
                <div className="about__paragraph">
                    <p>Total amount:</p>
                    <p> {totalInfo.stovesCount} Stoves</p>
                </div>
                <div className="about__paragraph">
                    <p>Total amount of starts:</p>
                    <p> {totalInfo.startCount} Times</p>
                </div>
                <div className="about__paragraph">
                    <p>Total running time:</p>
                    <p>{totalInfo.hoursCount} Hours</p>
                </div>
            </div>
            <footer>
                <p>Copyright © 2023 Byelex. All rights reserved.</p>
            </footer>
        </div>
    );
}

export default App;