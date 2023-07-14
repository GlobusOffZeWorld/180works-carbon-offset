import React, { FC, ReactElement, useState, useEffect } from 'react';
import Graph from './components/Graph';
import './App.css'
import Table from './components/Table';
import axios from 'axios'
import { Bar } from 'react-chartjs-2';

interface Details {
    stoves_num: number,
    date: string,
    work_num: number,
    work_time: number
}

interface District {
    district: string,
    count: number
}

interface GraphInfo {
    data: {
        labels: number[],
        datasets: [
            {
                label: string,
                data: number[],
                fill: boolean,
                borderColor: string,
                tension: number
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

const App: FC = () => {

    const [details, setDetails] = useState<Details[]>([{
        date: 'string',
        stoves_num: 1,
        work_num: 1,
        work_time: 1
    }])

    const [districts, setDistricts] = useState<District[]>([{
        district: "temp",
        count: 0
    }])


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

    for (const info of reversedDetails) {
        totalInfo.stovesCount += info.stoves_num
        totalInfo.startCount += info.work_num
        totalInfo.hoursCount += info.work_time
    }

    const days = [...Array(31).keys()]
    days.shift()

    const makeDiagram = (label: string, data: number[]): GraphInfo => {
        return {
            data: {
                labels: days,
                datasets: [
                    {
                        label: label,
                        data: data,
                        fill: false,
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

    useEffect(() => {
        getData();
        getDistricts();
    }, []);

    const slicedDistricts = districts.slice(0, 6)



    const barData = {
        labels: districts.map((el)=> {
            return el.district
        }),
        datasets: [
            {
                label: 'Count of stoves in each district',
                data: districts.map((el)=> {
                    return el.count
                }),
                backgroundColor: 'rgba(89, 84, 86, 0.3)',
                borderColor: 'rgb(89, 84, 86)',
                borderWidth: 1,
            },
        ],
    };

    const barOptions = {

    };










    const diagrams = [
        makeDiagram('Amount of working stoves', reversedDetails.map((detail: Details) => detail.stoves_num)),
        makeDiagram('Average number of launches', reversedDetails.map((detail: Details) => detail.work_num)),
        makeDiagram('Working hours', reversedDetails.map((detail: Details) => detail.work_time)),

    ]




    const missionInfo: string = `Использование печек существенно снижает потребление древесины, а следовательно и выброс CO2 в атмосферу.
    180.works хочет получить дополнительное финансирование за счет участия в программе Carbon Credits - ценные бумаги, которые выдаются за снижение выбросов CO2.
    Но для этого необходимо знать реальное использование печек.
    Сейчас компания исследует возможность встраивания в печки термодатчиков передающих данные по LoRaWAN протоколу.`

    console.log(districts)


    const mainSiteReference: ReactElement = <a href="https://180.works/#/carbon-offset">180.works</a>

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
                {diagrams.map(({ data, options }, index) => <div className="diagrams-container__chart" key={index}>
                    <Graph data={data} options={options} />
                </div>)}
                <div className="diagrams-container__chart">

                    <Bar data={barData} options={barOptions} />
                </div>
            </div>

            <div className="region-table">
                <table >
                    <thead>
                        <tr>
                            <th>Country</th>
                            <th>Furnace count</th>
                        </tr>
                    </thead>
                    <tbody>
                        {slicedDistricts.map((row, index) => (
                            <tr key={index}>
                                <td>{row.district}</td>
                                <td>{row.count}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {/* <Table /> */}
            </div>
            <div className="about">
                <div className="about__paragraph">
                    <p>Total amount:</p>
                    <p> {totalInfo.startCount} Stoves</p>
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